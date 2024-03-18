from rest_framework.decorators import APIView, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import logging
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime

logger = logging.getLogger(__name__)

@api_view(["POST"])
def login(request: Request):
    username, password = request.data.get("username"), request.data.get("password")
    if not username or not password:
        return Response(status=HTTP_400_BAD_REQUEST)
    else:
        user = authenticate(request=request, username=username, password=password)
        if user:
            token = RefreshToken.for_user(user)
            logger.info(f"{user.username} logged in")
            token_data = {
                "access": str(token.access_token),
                "refresh": str(token)
            }
            return Response(data=token_data, status=HTTP_200_OK)
        else:
            logger.info("Failed Login\nReason: Incorrect Credentials")
            return Response(status=HTTP_401_UNAUTHORIZED)

class UserAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        username, password, first_name, last_name, email = request.data.get("username"), request.data.get("password"), request.data.get("first_name"), request.data.get("last_name"), request.data.get("email")
        if not first_name or not email or not username or not password:
            logger.info("Failed Creating User\nReason: Incomplete Details")
            return Response(status=HTTP_400_BAD_REQUEST)
        elif User.objects.filter(username=username).exists():
            logger.info("Failed Creating User\nReason: Similar Username exists")
            return Response(status=HTTP_409_CONFLICT)
        else:
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            logger.info(f"{user.username} created")
            return Response(status=HTTP_201_CREATED)
    
    def delete(self, request: Request):
        user = request.user
        if user and user.is_active:
            try:
                user.delete()
                logger.info(f"{user.username} deleted")
                return Response(status=HTTP_204_NO_CONTENT)
            except Exception as e:
                logger.warn(f"Failed Deleting {user.username}\nReason: {e}")
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.info("Failed Deleting User\nReason: Unauthorised User")
            return Response(status=HTTP_401_UNAUTHORIZED)
    

class TaskAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        id = request.query_params.get('id')
        if not id:
            taskFilter = Task.objects.filter(user=request.user)
            tasks = TaskSerializer(taskFilter, many=True).data
            logger.info(f"{request.user.username} fetched Tasks")
            return Response({"tasks": tasks}, status=HTTP_200_OK)
        else:
            taskFilter = Task.objects.filter(id=id, user=request.user)
            if taskFilter.exists():
                task = TaskSerializer(taskFilter.get()).data
                logger.info(f"{request.user.username} fetched Task {id}")
                return Response(data=task, status=HTTP_200_OK)
            else:
                logger.info(f"{request.user.username} failed to fetch Task {id}\nReason: Task not found")
                return Response(status=HTTP_404_NOT_FOUND)

    def post(self, request: Request):
        title, description, deadline = request.data.get("title"), request.data.get("description"), request.data.get("deadline")
        if not title or not deadline:
            logger.info(f"{request.user.username} failed to create Task\nReason: Incomplete Details")
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%S.%f%z")
            task = Task(title=title, description=description, deadline=deadline, user=request.user)
            task.save()
            logger.info(f"{request.user.username} created Task {task.id}")
            return Response(data=TaskSerializer(task).data, status=HTTP_201_CREATED)
    
    def put(self, request: Request):
        title, description, deadline = request.data.get("title"), request.data.get("description"), request.data.get("deadline")
        id = request.query_params.get('id')
        if not (id and title and deadline):
            logger.info(f"{request.user.username} failed to update Task\nReason: Incomplete Details")
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            taskFilter = Task.objects.filter(id=id, user=request.user)
            if taskFilter.exists():
                task = taskFilter.get()
                task.title = title
                if description:
                    task.description = description
                task.deadline = deadline
                task.save()
                logger.info(f"{request.user.username} updated Task {task.id}")
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                logger.info(f"{request.user.username} failed to update Task\nReason: Task Not Found")
                return Response(status=HTTP_404_NOT_FOUND)
    
    def patch(self, request: Request):
        complete = request.data.get("complete")
        id = request.query_params.get("id")
        if not complete or not id:
            logger.info(f"{request.user.username} failed to change Task status\nReason: Incomplete Details")
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            taskFilter = Task.objects.filter(id=id, user=request.user)
            if taskFilter.exists():
                task = taskFilter.get()
                task.complete = complete
                task.save()
                logger.info(f"{request.user.username} updated Task {task.id} status")
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                logger.info(f"{request.user.username} failed to change Task status\nReason: Task Not Found")
                return Response(status=HTTP_404_NOT_FOUND)
    
    def delete(self, request: Request):
        id = request.query_params.get("id")
        if not id:
            logger.info(f"{request.user.username} failed to delete Task\nReason: Incomplete Details")
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            taskFilter = Task.objects.filter(id=id, user=request.user)
            if taskFilter.exists():
                task = taskFilter.get()
                task.delete()
                logger.info(f"{request.user.username} deleted Task {id}")
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                logger.info(f"{request.user.username} failed to delete Task\nReason: Task Not Found")
                return Response(status=HTTP_404_NOT_FOUND)
            