import redis
import base64
from PIL import Image
from io import BytesIO

# Connexion à Redis avec mot de passe
redis_client = redis.StrictRedis(
    host='172.20.10.11',
    port=6379,
    password='kaka',  # Remplacez par votre mot de passe
    decode_responses=False  # Garde les données sous forme de bytes
)

def transform_image(redis_key, output_path):
    try:
        # Récupérer l'image encodée en Base64 depuis Redis
        image_data = redis_client.get(redis_key)
        if not image_data:
            print("Image non trouvée dans Redis.")
            return
        
        print(f"Image récupérée avec succès pour la clé {redis_key}.")

        # Décoder l'image Base64
        decoded_image = base64.b64decode(image_data.split(b",")[1])

        # Charger l'image avec PIL
        image = Image.open(BytesIO(decoded_image))

        # Sauvegarder l'image au format JPG
        image.save(output_path, format="JPEG")
        print(f"L'image a été convertie et sauvegardée sous : {output_path}")

    except Exception as e:
        print(f"Erreur lors de la récupération ou de la conversion de l'image : {e}")

# Exemple d'utilisation
transform_image('image:id_q3pbu50x3', 'output_image.jpg')
