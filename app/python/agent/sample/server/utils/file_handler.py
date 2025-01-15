import os
import aiofiles

class FileHandler:
    async def save_temp_file(self, file, destination: str) -> str:
        file_location = os.path.join(destination, file.filename)
        async with aiofiles.open(file_location, "wb") as f:
            await f.write(await file.read())
        return file_location

    def delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)