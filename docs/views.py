from django.core.mail import send_mail
import time
from PIL import Image
from rest_framework import status
import boto3
import os
from django.core import exceptions
import hashlib
import json
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import (
    DocSerializer,
    FileCabinetSerializer,
    RegSerializer,
    BlockSerializer
)
from users.serializers import (
    UserSerializer,
    NotifSerializer,
    send_notif,
)
from users.models import (
    Notif,
    User
)
from .permissions import (
    CustomIsAuthenticated,
    CustomIsAuthenticated2,
    CustomIsAuthenticated3,
    CustomIsAuthenticated4,
)
from .models import (
    Doc,
    FileCabinet,
    Reg,
    Block
)
from rest_framework import (
    generics,
    mixins,
    viewsets,
    permissions,
    views
)
from edc.EDC import EDC
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from datetime import timedelta
from six.moves import urllib
import re
# Для FTP сервера
from ftp import FTPStorage, FTPStorageFile
fs = FTPStorage()

class DocViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с документами.
    При создании документа обязательно указывать user_id, потому 
    что создается еще запись Notif, где есть созданный документ и 
    указанный пользователь в user_id.
    Права - админ или владелец.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated,)

    def list(self, request):
        queryset = Doc.objects.filter(common=True)
        serializer = DocSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            notif = Notif.objects.create(
                user_id=request.data["user_id"], 
                doc_id=serializer.data["id"],
                status=0,
                date=timezone.now()
            )
            serializerNotif = NotifSerializer(notif)
            return Response(serializerNotif.data)
        except Exception as e:
            raise exceptions.ValidationError(str(e))

class DownloadFile(generics.RetrieveAPIView):
    '''
    Скачать файл.
    Права - нет (они проверяются на сервере генерации подписи).
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated3,)

    def get(self, request, pk):
        doc = Doc.objects.get(id=self.kwargs['pk'])
        filename = str(doc.file)
        try:
            filename = re.sub('\\', '/', filename)
        except:
            pass
        fsFile = FTPStorageFile('/'+filename, fs, 'rw')
        f = open('staticfiles/'+filename, 'wb')
        file = fsFile.read()
        f.write(file)

        f.close()
        fsFile.close()

        return Response({'file': filename})

class DownloadSign(generics.RetrieveAPIView):
    '''
    Скачать файл.
    Права - нет (они проверяются на сервере генерации подписи).
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated3,)

    def get(self, request, pk):
        doc = Doc.objects.get(id=self.kwargs['pk'])

        filename = str(doc.file).split('\\')[1].split('.')[0]
        filename = 'sign/' + filename + '.txt'

        ff = open('staticfiles/'+filename, 'w')
        ff.write(doc.signature)
        ff.close()

        return Response({'file': filename})

class DeleteFileFromLocal(generics.RetrieveAPIView):
    '''
    Скачать файл.
    Права - нет (они проверяются на сервере генерации подписи).
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated3,)

    def get(self, request, pk, type):
        doc = Doc.objects.get(id=self.kwargs['pk'])

        try:
            if self.kwargs['type'] == 'file':
                os.remove('staticfiles/'+str(doc.file))
            else:
                filename = str(doc.file).split('\\')[1].split('.')[0]
                filename = 'staticfiles/sign/' + filename + '.txt'
                os.remove(filename)
        except Exception as e:
            print(str(e))

        return Response({'status': 200})

class FileCabinetViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с картотеками.
    '''
    serializer_class = FileCabinetSerializer
    queryset = FileCabinet.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated4,)

class RegViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с приставками к регистрационным номерам.
    '''
    serializer_class = RegSerializer
    queryset = Reg.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated4,)

class BlockViewSet(viewsets.ModelViewSet):
    '''
    Универсальное представление для работы с блоками.
    '''
    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated4,)

def СheckSign(request, pk):
    doc = Doc.objects.get(id=pk)
    block = Block.objects.get(id=doc.hash_id)
    try:
        previous_block = Block.objects.get(id=doc.hash_id-1)
        temp = {
            'id': block.id,
            'data': doc.signature,
            'previous_hash': previous_block.hash
        }
    except:
        temp = {
            'id': block.id,
            'data': doc.signature
        }
    block_string = json.dumps(temp, sort_keys=True).encode()
    hash = hashlib.sha256(block_string).hexdigest()
    if block.hash != hash:
        return JsonResponse({'check': 'Подпись НЕ достоверна!'}, status=200)
    return JsonResponse({'check': 'Подпись достоверна.'}, status=200)
    
class AddSignature(generics.ListAPIView):
    '''
    Добавить подпись к документу. Принимает id документа.
    Права - админ или владелец нотифа, который с этим доком и 
    который надо подписать.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated2,)

    def get_queryset(self):
        # Найти нужный документ
        doc = Doc.objects.get(id=self.kwargs['pk'])
        first = self.kwargs['first']
        del self.kwargs['first']

        # Найти нотиф, который с этим документом и
        # пользователь - владелец документа
        notifOwner = Notif.objects.get(
            doc_id=doc.id,
            status=0
        )

        # Функция генерации подписи
        edc = EDC()
    
        if first == '1':
            fileLocal = DownloadFile.as_view()(self.request._request, **self.kwargs)
            file = open('staticfiles/'+str(doc.file), 'rb')
            signature = edc.signFile(file, notifOwner.user.username)
            file.close()
            os.remove('staticfiles/'+str(doc.file))
        if first == '0':
            fileLocal = DownloadSign.as_view()(self.request._request, **self.kwargs)
            filename = str(doc.file).split('\\')[1].split('.')[0]
            filename = 'staticfiles/sign/' + filename + '.txt'
            file = open(filename, 'rb')
            signature = edc.signFile(file, notifOwner.user.username)
            file.close()
            os.remove(filename)

        # Добавить подпись
        doc.signature = signature
        doc.save()
        id = doc.id
        
        if first == '0':
            # Найти нотиф, который с этим документом и
            # где очередь подписывать и изменить на "подписано"
            try:
                notif = Notif.objects.get(
                    doc_id=doc.id,
                    status=2
                )
                # notif.status = 3
                notif.date = timezone.now()
                notif.save()
            except: pass
            # Найти следующий нотиф, который с этим документом и
            # где очередь = очередь+1
            try:
                notifNext = Notif.objects.get(
                    doc_id=doc.id,
                    status=1,
                    queue=notif.queue+1
                )
                notifNext.status = 2
                notifNext.date = timezone.now()
                notifNext.save()
            # Если следующего нотифа нет, значит подпись больше не нужна
            except:
                doc.signature_end = True
                doc.save()

        if first == '1':
            try:
                notifNext = Notif.objects.get(
                    doc_id=id,
                    status=2,
                    queue=0
                )
                notifNext.save()
            # Если нулевого нотифа нет, значит подпись не нужна
            except:
                doc.signature_end = True
                doc.save()
        
        if len(Block.objects.all()) == 0:
            temp = {
                'id': block.id,
                'data': block.data
            }
            block_string = json.dumps(temp, sort_keys=True).encode()
            block = Block.objects.create(
                data=signature,
                hash = hashlib.sha256(block_string).hexdigest()
            )
        else:
            last_block = Block.objects.last()
            temp = {
                'id': last_block.id+1,
                'data': signature,
                'previous_hash': last_block.hash
            }
            block_string = json.dumps(temp, sort_keys=True).encode()
            block = Block.objects.create(
                data=signature,
                hash=hashlib.sha256(block_string).hexdigest(),
                previous_hash=last_block.hash
            )
        doc.hash_id = block.id
        doc.save()

        doc = Doc.objects.filter(id=self.kwargs['pk'])
        serializer = DocSerializer(doc)
        return doc

class CancelSignature(viewsets.ModelViewSet):
    '''
    Отменить подпись и удалить все подписи.
    Права - админ или владелец нотифа, который с этим доком и 
    который надо подписать.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated2,)

    def cancel_signature(self, request, pk):
        # Найти нужный документ
        doc = Doc.objects.get(id=self.kwargs['pk'])
        # Поменять данные
        if ('file' in request.data):
            doc.cancel_file = request.data['file']
        doc.signature = None
        doc.cancel_description = request.data['cancel_description']
        doc.save()

        # Теперь тот, кто должен был подписать, 
        # становится "отказчиком"
        notifCancel = Notif.objects.get(
            doc_id=doc.id,
            status=2,
        )
        notifCancel.date = timezone.now()
        notifCancel.status = 7
        notifCancel.save()

        return Response(DocSerializer(doc).data)

class SignatureAgain(generics.ListAPIView):
    '''
    Начать цепочку подписей снова.
    Права - админ или владелец документа.
    '''
    serializer_class = DocSerializer
    queryset = Doc.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomIsAuthenticated,)

    def get_queryset(self):
        id = id = self.kwargs['pk']
        # Найти нужный документ, убрать комментарий отказа
        doc = Doc.objects.get(id=id)
        doc.cancel_description = None
        doc.signature_end = False
        doc.save()

        # Владелец должен подписать
        notifOwner = Notif.objects.get(
            doc_id=id,
            status=0,
        )
        self.kwargs['first'] = '1'
        doc = AddSignature.as_view()(self.request._request, **self.kwargs)
        # doc = list(doc.data)
        # print('doc', doc)

        # Все статусы 2, 3 и 7 с этим документом 
        # превратить в статус 1 (хотя бы один должен быть)
        notif = Notif.objects.filter(
            doc_id=id,
            status=2,
        )
        notif = notif | Notif.objects.filter(
            doc_id=id,
            status=3,
        )
        notif = notif | Notif.objects.filter(
            doc_id=id,
            status=7,
        )
        for i, n in enumerate(notif):
            n.status = 1
            notif[i].save()

        # Отправить уведомление человеку, который должен
        # подписать и нулевой в очереди
        try:
            notif0 = Notif.objects.get(
                doc_id=id,
                status=1,
                queue=0,
            )
            notif0.status = 2
            notif0.save()
            send_notif(notif0)
        except: pass

        return Doc.objects.filter(id=id)
