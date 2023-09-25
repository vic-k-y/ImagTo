import requests
import time
from io import BytesIO
from PIL import Image


url = "https://api.prodia.com/v1/sd/generate"
def api_call_send(model,promt,negative_prompt,aspect_ratio,steps,cfg_scale,seed,upscale,sampler):
    payloadsend = {
        "model": model,
        "prompt": promt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "seed": seed,
        "upscale": upscale,
        "sampler": sampler,
        "aspect_ratio": aspect_ratio
    }
    
    headerssend = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": "596e85a1-b3ae-49fb-ae11-cee1c4f78eee"
    }

    response = requests.post(url, json=payloadsend, headers=headerssend)
    #print(response.text)
    return response.json()


def retrive_image(job_id):
    url = "https://api.prodia.com/v1/job/" + str(job_id)

    headers = {
        "accept": "application/json",
        "X-Prodia-Key": "596e85a1-b3ae-49fb-ae11-cee1c4f78eee"
    }

    response = requests.get(url, headers=headers)
    #print(response.text)
    result = response.json()
    
    while result["status"] != "succeeded":  # wait until the image is ready
        result = requests.get(url, headers=headers).json()
        for i in range(11):
            if i <9:
                time.sleep(1)
            else:
                break
        
    return result["imageUrl"]

#save the image to the current directory
def save_image(image_url):
    image = requests.get(image_url)
    #open("image.png", "wb").write(image.content)
    img_name = "image_"+time.strftime("%H%M%S",time.localtime())+".png"
    with open(img_name, "wb") as f:
        f.write(image.content)


def generate_image(prompt):
    job_id = api_call_send(prompt)
    #print(job_id["job"])
    id = job_id["job"]
    image_url = retrive_image(id)
    save_image(image_url)

def generate_gradio(model,promt,negative_prompt,aspect_ratio,steps,cfg_scale,seed,upscale,sampler):
    job_id = api_call_send(model,promt,negative_prompt,aspect_ratio,steps,cfg_scale,seed,upscale,sampler)
    #print(job_id["job"])
    id = job_id["job"]
    image_url = retrive_image(id)
    image = Image.open(BytesIO(requests.get(image_url).content))
    return image



models = [
  "absolutereality_V16.safetensors [37db0fc3]",
  "absolutereality_v181.safetensors [3d9d4d2b]",
  "analog-diffusion-1.0.ckpt [9ca13f02]",
  "anythingv3_0-pruned.ckpt [2700c435]",
  "anything-v4.5-pruned.ckpt [65745d25]",
  "anythingV5_PrtRE.safetensors [893e49b9]",
  "AOM3A3_orangemixs.safetensors [9600da17]",
  "childrensStories_v13D.safetensors [9dfaabcb]",
  "childrensStories_v1SemiReal.safetensors [a1c56dbb]",
  "childrensStories_v1ToonAnime.safetensors [2ec7b88b]",
  "cyberrealistic_v33.safetensors [82b0d085]",
  "deliberate_v2.safetensors [10ec4b29]",
  "deliberate_v3.safetensors [afd9d2d4]",
  "dreamlike-anime-1.0.safetensors [4520e090]",
  "dreamlike-diffusion-1.0.safetensors [5c9fd6e0]",
  "dreamlike-photoreal-2.0.safetensors [fdcf65e7]",
  "dreamshaper_6BakedVae.safetensors [114c8abb]",
  "dreamshaper_7.safetensors [5cf5ae06]",
  "dreamshaper_8.safetensors [9d40847d]",
  "edgeOfRealism_eorV20.safetensors [3ed5de15]",
  "EimisAnimeDiffusion_V1.ckpt [4f828a15]",
  "elldreths-vivid-mix.safetensors [342d9d26]",
  "epicrealism_naturalSinRC1VAE.safetensors [90a4c676]",
  "ICantBelieveItsNotPhotography_seco.safetensors [4e7a3dfd]",
  "juggernaut_aftermath.safetensors [5e20c455]",
  "lyriel_v16.safetensors [68fceea2]",
  "mechamix_v10.safetensors [ee685731]",
  "meinamix_meinaV9.safetensors [2ec66ab0]",
  "meinamix_meinaV11.safetensors [b56ce717]",
  "openjourney_V4.ckpt [ca2f377f]",
  "portraitplus_V1.0.safetensors [1400e684]",
  "Realistic_Vision_V1.4-pruned-fp16.safetensors [8d21810b]",
  "Realistic_Vision_V2.0.safetensors [79587710]",
  "Realistic_Vision_V4.0.safetensors [29a7afaa]",
  "Realistic_Vision_V5.0.safetensors [614d1063]",
  "redshift_diffusion-V10.safetensors [1400e684]",
  "revAnimated_v122.safetensors [3f4fefd9]",
  "rundiffusionFX25D_v10.safetensors [cd12b0ee]",
  "rundiffusionFX_v10.safetensors [cd4e694d]",
  "sdv1_4.ckpt [7460a6fa]",
  "v1-5-pruned-emaonly.safetensors [d7049739]",
  "shoninsBeautiful_v10.safetensors [25d8c546]",
  "theallys-mix-ii-churned.safetensors [5d9225a4]",
  "timeless-1.0.ckpt [7c4971d4]",
  "toonyou_beta6.safetensors [980f6b15]"
]

sampler = ["Euler","Eular a","Heun","DPM++ 2S a",
           "DPM++ 2S a Karras","DPM++ 2M","DPM++ 2M Karras",
           "DPM++ SDE","DPM++ SDE Karras","DPM fast","DDim","PLMS"]

ex_prompt1="Deep photo, light background, iphone 12 camera, poor taken photo, shadows, 20yo girl, messy long hair, perfect face and body, toned body, small body, 5' tall, flirty smile, big breasts, breasts size (30DD), small waist, white lace coctktail short dress, high wicker sandals, light photo, sunset, (indirect light), harsh camera flash, ((light brown eyes)), beach weddig, beach party"
ex_nprompt1="asian, chinese, afro american, error, cropped, ugly, duplicate, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, black and white filter, green color,nude, erotic"

galimg = ["gal_images/image (1).png","gal_images/image (2).png",
          "gal_images/image (3).png","gal_images/image (5).png",
          "gal_images/image (6).png","gal_images/image (7).png","gal_images/image (8).png",
          "gal_images/image (9).png","gal_images/image (10).png","gal_images/image (11).png",
          "gal_images/image.png","gal_images/image (4).png"]

ex_prompt2 = "Masterpiece, Stunning, Best quality, a captivating space-themed artwork featuring the ethereal beauty of swirling nebulas and twinkling stars with an astronaut in it dark, blue themed"
ex_nprompt2 = "(Naked, Nude, NSFW), (text), (signatures), lowres, (worst quality), (low quality), (normal quality), Out of Frame, blurry, jpeg artifacts, watermark, logo, letters, username, words, cropped"

ex_prompt3 = "portrait of a Lumberjack woman with huge beautiful braid, wearing tight-fitting outfit, intricate action pose, Oil paint, ancient, illuminated by the light of twilight, with a backdrop of a big oldest house and ancient forest., Mysterious, brilliant art by Allan Jabbar, Yann Dalon, Toni Infante, Amr Elshamy"
ex_nprompt3 = "(Naked, Nude, NSFW), (text), (signatures), lowres, (worst quality), (low quality), (normal quality), Out of Frame, blurry, jpeg artifacts, watermark, logo, letters, username, words, cropped"

ex_prompt4 = "medium shot full body! ! highly detailed stunning image of ghost sorcerer, octane render, unreal engine 5, 8k, hyper realistic, realistic, soft illumination, surrounded in dask wispy smoke! ! trending on artstation"
ex_nprompt4 = " "