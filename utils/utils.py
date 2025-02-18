import os


class Utils:
    @staticmethod
    async def is_whitelisted(user_id: int) -> bool:
        with open("whitelist.txt", "r") as f:
            whitelisted_users = f.read().splitlines()
            return str(user_id) in whitelisted_users

    @staticmethod
    async def add_to_whitelist(user_id: int) -> bool:
        with open("whitelist.txt", "r+") as f:
            whitelisted_users = f.read().splitlines()
            if str(user_id) in whitelisted_users:
                return False
            f.write(str(user_id) + "\n")
            return True
        
    @staticmethod
    async def remove_from_whitelist(user_id: int) -> bool:
        with open("whitelist.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            user_removed = False
            for line in lines:
                if str(user_id) not in line.strip():
                    f.write(line)
                else:
                    user_removed = True
            f.truncate()
            return user_removed
        

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')