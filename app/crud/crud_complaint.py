import os
import uuid
from app.db.init_db import database
from app.models import complaint, RoleType, State
from app.services.s3 import S3Service
from app.services.ses import SESService
from app.constants import TEMP_FILE_FOLDER
from app.utils.helpers import decode_photo

s3 = S3Service()
ses = SESService()

class CrudComplaint:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.status == State.pending)
        return await database.fetch_all(q)


    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo")
        extention = complaint_data.pop("extention")
        name = f"{uuid.uuid4()}.{extention}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data["photo_url"] = s3.upload(path, name, extention)
        os.remove(path)
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))
    

    @staticmethod
    async def delete_complaint(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))


    @staticmethod
    async def approve(id_):
        await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.approved))
        email = await database.fetch_one(complaint.select().where(complaint.c.id == id_))
        print(email)
        ses.send_mail(
            "Complaint aproved!", 
            ["pankaj.karki.786@gmail.com"], 
            "Congrats! Your claim is approved check your bank account in 2 days for your refund"
            )


    @staticmethod
    async def reject(id_):
        await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.rejected))

