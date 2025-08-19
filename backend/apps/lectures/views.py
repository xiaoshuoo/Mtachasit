from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpRequest
from .models import Lecture, LectureCategory
import os


def is_staff(user):
    return user.is_staff


class LectureListView(ListView):
    model = Lecture
    template_name = 'blog/lecture_page.html'
    context_object_name = 'lectures'
    paginate_by = 10

    def get_queryset(self):
        queryset = Lecture.objects.filter(is_active=True)
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LectureCategory.objects.all()
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['selected_category'] = get_object_or_404(LectureCategory, slug=category_slug)
        return context


@login_required
@user_passes_test(is_staff)
def create_lecture(request: HttpRequest):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category_id = request.POST.get('category')

        if not title or not content:
            messages.error(request, 'Заполните все обязательные поля.')
            return redirect('blog:lectures')

        lecture = Lecture.objects.create(title=title, content=content, author=request.user)
        if category_id:
            try:
                category = LectureCategory.objects.get(id=category_id)
                lecture.category = category
                lecture.save()
            except LectureCategory.DoesNotExist:
                pass
        messages.success(request, f'Лекция "{title}" успешно создана.')
        return redirect('blog:lectures')
    return redirect('blog:lectures')


@login_required
@user_passes_test(is_staff)
def edit_lecture(request: HttpRequest, pk: int):
    lecture = get_object_or_404(Lecture, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category_id = request.POST.get('category')

        if not title or not content:
            messages.error(request, 'Заполните все обязательные поля.')
            return redirect('blog:lectures')

        lecture.title = title
        lecture.content = content
        if category_id:
            try:
                category = LectureCategory.objects.get(id=category_id)
                lecture.category = category
            except LectureCategory.DoesNotExist:
                lecture.category = None
        else:
            lecture.category = None
        lecture.save()
        messages.success(request, f'Лекция "{title}" успешно обновлена.')
        return redirect('blog:lectures')
    return redirect('blog:lectures')


@login_required
@user_passes_test(is_staff)
def delete_lecture(request: HttpRequest, pk: int):
    lecture = get_object_or_404(Lecture, pk=pk)
    if request.method == 'POST':
        title = lecture.title
        lecture.delete()
        messages.success(request, f'Лекция "{title}" успешно удалена.')
    return redirect('blog:lectures')


@login_required
@user_passes_test(is_staff)
def import_lecture(request: HttpRequest):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            messages.error(request, 'Выберите файл для импорта.')
            return redirect('blog:lectures')
        if not uploaded_file.name.endswith('.txt'):
            messages.error(request, 'Поддерживаются только текстовые файлы (.txt).')
            return redirect('blog:lectures')
        try:
            content = uploaded_file.read().decode('utf-8')
            title = os.path.splitext(uploaded_file.name)[0]
            Lecture.objects.create(title=title, content=content, author=request.user)
            messages.success(request, f'Лекция "{title}" успешно импортирована.')
        except Exception as e:
            messages.error(request, f'Ошибка при импорте файла: {str(e)}')
    return redirect('blog:lectures')


@login_required
@user_passes_test(is_staff)
def import_lectures_from_directory(request: HttpRequest):
    if request.method == 'POST':
        directory_path = request.POST.get('directory_path', '').strip()
        if not directory_path:
            messages.error(request, 'Укажите путь к директории.')
            return redirect('blog:lectures')
        if not os.path.exists(directory_path):
            messages.error(request, 'Указанная директория не существует.')
            return redirect('blog:lectures')
        imported_count = 0
        errors: list[str] = []
        try:
            for filename in os.listdir(directory_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(directory_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            title = os.path.splitext(filename)[0]
                            if not Lecture.objects.filter(title=title).exists():
                                Lecture.objects.create(title=title, content=content, author=request.user)
                                imported_count += 1
                            else:
                                errors.append(f'Лекция "{title}" уже существует')
                    except Exception as e:
                        errors.append(f'Ошибка при обработке файла {filename}: {str(e)}')
            if imported_count > 0:
                messages.success(request, f'Успешно импортировано {imported_count} лекций.')
            for error in errors[:5]:
                messages.warning(request, error)
        except Exception as e:
            messages.error(request, f'Ошибка при обработке директории: {str(e)}')
    return render(request, 'blog/import_directory.html')


