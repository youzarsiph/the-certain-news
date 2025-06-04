# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create new Django project and configure the settings
RUN django-admin startproject core
RUN cp -r al_yaqeen core

# Configure settings
RUN echo "AUTH_USER_MODEL = 'users.User'" >> core/settings.py
RUN echo "INSTALLED_APPS += [" >> core/settings.py
RUN echo "    'al_yaqeen'," >> core/settings.py
RUN echo "    'al_yaqeen.ai'," >> core/settings.py
RUN echo "    'al_yaqeen.articles'," >> core/settings.py
RUN echo "    'al_yaqeen.categories'," >> core/settings.py
RUN echo "    'al_yaqeen.comments'," >> core/settings.py
RUN echo "    'al_yaqeen.reactions'," >> core/settings.py
RUN echo "    'al_yaqeen.ui'," >> core/settings.py
RUN echo "    'al_yaqeen.users'," >> core/settings.py
RUN echo "    'corsheaders'" >> core/settings.py
RUN echo "    'rest_wind'," >> core/settings.py
RUN echo "    'django_filters'," >> core/settings.py
RUN echo "    'rest_framework'" >> core/settings.py
RUN echo "]" >> core/settings.py

# Setup URLConf
RUN echo "from django.urls import include" >> core/urls.py
RUN echo "urlpatterns += [path('', include('al_yaqeen.urls'))]" >> core/urls.py

# Run migrations
RUN cd core && python manage.py migrate


WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi"]
