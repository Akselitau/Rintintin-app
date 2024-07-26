import boto3
import os

# Configuration AWS
AWS_ACCESS_KEY_ID = 'AKIA6GBMEIQNYROIG4PR'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'eu-west-3'
S3_BUCKET_NAME = 'rintintin-bucket'
S3_KEY = 'exemple.png'  # Changez le nom de fichier ici

# Chemin local du fichier à uploader
local_file_path = 'exemple.png'  # Remplacez par le chemin de votre fichier

# Initialiser le client S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

try:
    # Uploader le fichier vers S3
    s3_client.upload_file(
        local_file_path,
        S3_BUCKET_NAME,
        S3_KEY
    )

    # Générer l'URL publique du fichier
    file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{S3_KEY}"
    print("Fichier uploadé avec succès ! URL:", file_url)

except Exception as e:
    print("Erreur lors de l'upload du fichier:", str(e))
