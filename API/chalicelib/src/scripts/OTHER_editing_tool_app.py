# import boto3
# from chalice import Chalice, Response
# from PIL import Image
# from PIL import ImageOps
# import requests
# from io import BytesIO
# import uuid

# app = Chalice(app_name='image_processing')
# s3 = boto3.client('s3')
# BUCKET_NAME = 'mockup-product'

# def ensure_scheme(url):
#     if not url.startswith(('http://', 'https://')):
#         return 'http:' + url
#     return url

# def resize_image(image, size, keep_aspect_ratio=True):
#     if keep_aspect_ratio:
#         original_width, original_height = image.size
#         desired_width, desired_height = size
#         aspect_ratio_original = original_width / original_height
#         aspect_ratio_desired = desired_width / desired_height

#         if aspect_ratio_desired > aspect_ratio_original:
#             new_height = desired_width / aspect_ratio_original
#             new_size = (desired_width, int(new_height))
#         else:
#             new_width = desired_height * aspect_ratio_original
#             new_size = (int(new_width), desired_height)
#     else:
#         new_size = size
    
#     return image.resize(new_size, Image.ANTIALIAS)

# def resize_background_image(image, container_size):
#     # Calcul du ratio de l'image et du conteneur
#     image_ratio = image.width / image.height
#     container_ratio = container_size[0] / container_size[1]

#     if image_ratio > container_ratio:
#         # L'image est plus large que le conteneur
#         scaled_height = container_size[1]
#         scaled_width = int(image_ratio * scaled_height)
#     else:
#         # L'image est plus haute que le conteneur ou a le même ratio
#         scaled_width = container_size[0]
#         scaled_height = int(scaled_width / image_ratio)

#     # Redimensionnement de l'image pour qu'elle couvre le conteneur
#     return image.resize((scaled_width, scaled_height), Image.ANTIALIAS)

# @app.route('/merge-images', methods=['POST'], content_types=['application/json'])
# def merge_images():
#     request = app.current_request
#     body = request.json_body

#     img1_url = ensure_scheme(body.get('background_image_url'))
#     img2_url = ensure_scheme(body.get('product_image_url'))
#     position = tuple(body.get('position', [0, 0]))
#     size = tuple(body.get('size', [100, 100]))
#     container_size = tuple(body.get('container_size', [500, 500]))  # Valeur par défaut si non spécifié

#     try:
#         img1_response = requests.get(img1_url)
#         img2_response = requests.get(img2_url)
#         img1 = Image.open(BytesIO(img1_response.content))
#         img2 = Image.open(BytesIO(img2_response.content))

#         # Redimensionner l'image de fond pour qu'elle corresponde à la taille du conteneur front-end
#         img1_resized = resize_background_image(img1, container_size)

#         # Redimensionner l'image de premier plan tout en conservant son rapport d'aspect
#         img2_resized = resize_image(img2, size)

#         result_image = Image.new('RGBA', container_size)  # Utilise container_size au lieu de background_size
#         result_image.paste(img1_resized, (0, 0))
#         result_image.paste(img2_resized, position, img2_resized if img2_resized.mode == 'RGBA' else None)

#         img_bytes = BytesIO()
#         result_image.save(img_bytes, format='PNG')
#         img_bytes.seek(0)

#         filename = f"{uuid.uuid4()}.png"
#         s3.upload_fileobj(img_bytes, BUCKET_NAME, filename, ExtraArgs={'ContentType': 'image/png'})
#         image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

#         return Response(body=image_url, status_code=200, headers={'Content-Type': 'text/plain'})

#     except Exception as e:
#         return Response(body=f"Error: {str(e)}", status_code=500)
