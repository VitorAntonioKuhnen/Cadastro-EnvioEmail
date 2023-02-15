from asyncio.windows_events import NULL
from random import random
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User

#Import do Envio de E-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def gerarSenha():
    numeros = [1,2,3,4,5,6,7,8,9,0]
    letrasMinu = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']    
    letrasMaiu = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    characters = ['!','@','#','$','%','&','*',',','.','?']
    senha = random(letrasMinu, 3)
    senha = random(letrasMaiu, 2)
    senha = random(numeros, 3)
    senha = random(characters,2)
    print(senha)

    return senha


def enviaEmail(email, nomeCompleto, user, senha):
    #The mail addresses and password
    sender_address = 'viniciusmschutz.vs@gmail.com'
    sender_pass = 'wjyydyuygdolgbuw'
    receiver_address = email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Teste de envio de e-mail'   #The subject line

    mail_content = 'Olá ' + nomeCompleto + ' abaixo segue seus dados para acesso ao nosso site!!' + '\n\nUsuario: ' + user + '\nSenha: ' + senha + '\n\n\nAtenciosamente Equipe'

    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return 'Email Enviado'



def login(request):
    if "login" in request.POST:
        usuario = request.POST.get('usuario')
        check = auth.authenticate(request, username=usuario)

        if check is not None:
            auth.login(request, check)

            if request.user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('inicio')
        else:
            messages.error(request, 'Usuario ou Senha Incorreto!!')
            return redirect('login')
    elif "cadastro" in request.POST:
        nome = request.POST.get('nome').strip()
        email = request.POST.get('email').strip()
        usuario = request.POST.get('usuario').strip()
        if len(nome) is not NULL:
                if len(email) is not NULL:
                    if len(usuario) >= 3:
                        # passwords = gerarSenha
                        passwords = 'Senha123'
                        User.objects.create_user(username=usuario, password=passwords, first_name=nome , email=email)
                        print(enviaEmail(email,nome,usuario,passwords))
                        return redirect('login')
                    else:
                        messages.error(
                            request, 'Usuario informado é menor que 3 caracters!!')
                        return redirect('cadastro')
                else:
                    messages.error(
                        request, 'É necessario informar um Email!!')
                    return redirect('cadastro')
        else:
            messages.error(
                request, 'É necessario informar o Primeiro Nome!!')
            return redirect('cadastro')
    else:
        return render(request, 'log_cad/index.html')


    