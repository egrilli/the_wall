from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from app_wall.models import User, Message , Comment
from app_wall.decorators import *

def index(request):

    return render(request, 'index.html')


def registro(request):
    if request.method == "POST":
        errors = User.objects.validador_basico(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            request.session['registro_nombre'] =  request.POST['firstname']
            request.session['registro_apellido'] =  request.POST['lastname']
            request.session['registro_email'] =  request.POST['email']

        else:
            request.session['registro_nombre'] = ""
            request.session['registro_apellido'] = ""
            request.session['registro_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                firstname = request.POST['firstname'],
                lastname=request.POST['lastname'],
                email=request.POST['email'],
                dateborn=request.POST['dateborn'],
                password=password_encryp
            )

            messages.success(request, "El usuario fue agregado con exito.")
            
        return redirect("/")
    else:
        return render(request, 'index.html')


def logearse(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                usuario = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email,
                    "rol":log_user.rol
                }

                request.session['usuario'] = usuario
                messages.success(request, "Logeado correctamente.")
                return redirect("/wall")
            else:
                messages.error(request, "Password o Email  malas.")
        else:
            messages.error(request, "Email o password malas.")

        return redirect("/logearse")
    else:
        return render(request, 'index.html')

    return render(request, 'index.html')



@login_required
def wall(request):
    context = {
        'user': User.objects.get(id=request.session['usuario']['id']),
        'all_messages': Message.objects.all(),
    }

    return render(request, 'wall.html',context)


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        messages.error(request, "Sesion Cerrada")
    return redirect("/")


@login_required
def colaborador(request):
    return render(request, 'colaborador.html')


@login_required
@val_admin
def administrador(request):
    return render(request, 'administrador.html')



def nuevoMensaje(request):
    print(request.POST)
    newmpost= Message.objects.create(message=request.POST['post'],user=User.objects.get(id=request.session['usuario']['id']))
    return redirect("/wall")

def borrarMensaje(request):
    print(request.POST)
    delete_post = Message.objects.get(id=request.POST['delete_post_id'])
    delete_post.delete()
    return redirect('/wall')

def comentarMensaje(request):
    print(request.POST)
    user = User.objects.get(id=request.POST['user_id'])
    message = Message.objects.get(id=request.POST['post_id'])
    Comment.objects.create(comment=request.POST['comment'], message=message, user=user)
    return redirect('/wall')


