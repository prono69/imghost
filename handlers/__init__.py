from db import save_image_url  

async def handle_photo(client, message):
    
    file_url = "example_file_url"  
    save_image_url(file_url)  
