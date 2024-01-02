from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "123456"

hashed_password = bcrypt_context.hash(password)
hashed_password1 = bcrypt_context.hash(password)
hashed_password2 = bcrypt_context.hash(password)
hashed_password3 = bcrypt_context.hash(password)
hashed_password4 = bcrypt_context.hash(password)
hashed_password5 = bcrypt_context.hash(password)
hashed_password10 = bcrypt_context.hash(password)
hashed_password11 = bcrypt_context.hash(password)
hashed_password12 = bcrypt_context.hash(password)
hashed_password13 = bcrypt_context.hash(password)
hashed_password14 = bcrypt_context.hash(password)
hashed_password15 = bcrypt_context.hash(password)


print(f"{hashed_password} \n{hashed_password1} \n{hashed_password2} \n{hashed_password3} \n{hashed_password4} \n{hashed_password5} \n{hashed_password10} \n{hashed_password11} \n{hashed_password12} \n{hashed_password13} \n{hashed_password14} \n{hashed_password15}")

