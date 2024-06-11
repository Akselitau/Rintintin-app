# import os
# import boto3
# from chalice import Chalice, Response
# from PIL import Image
# from PIL import ImageOps
# import requests
# from io import BytesIO
# import uuid
# import openai
# import re


# app = Chalice(app_name='image_processing')
# s3 = boto3.client('s3')
# BUCKET_NAME = 'mockup-product'

# # Set the OpenAI API key from the environment variable
# openai.api_key = 'sk-proj-n50OOBIbioHH8HunuZiiT3BlbkFJme45ktXV6ftlTWMNuEjD'
# if not openai.api_key:
#     raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

# def parse_openai_response(ideas_text):
#     # Match titles and fields explicitly
#     pattern = re.compile(
#         r"Title:\s*(.*?)(?:\s*Description:\s*(.*?))?\s*"
#         r"MRR:\s*(.*?)(?:\s*Competitors:\s*(.*?))?\s*"
#         r"Goods:\s*(.*?)(?:\s*Complexity:\s*(.*?))?\s*(?=(Title:|$))",
#         re.DOTALL
#     )

#     matches = pattern.findall(ideas_text)
#     processed_ideas = []

#     for match in matches:
#         title, description, mrr, competitors, goods, complexity, _ = match
#         # Creating a dictionary while handling empty fields
#         idea_dict = {
#             'title': title.strip(),
#             'description': description.strip() if description else "No description provided.",
#             'mrr': mrr.strip() if mrr else "No MRR provided.",
#             'competitors': competitors.strip() if competitors else "No competitors listed.",
#             'goods': goods.strip() if goods else "No benefits mentioned.",
#             'complexity': complexity.strip() if complexity else "No complexities listed."
#         }
#         processed_ideas.append(idea_dict)

#     return processed_ideas


# def call_openai(category, num_developers):
#     prompt = f"""Generate 3 SaaS ideas in English for {num_developers} developer(s) in the category of {category}. 
#     Please ensure that each idea follows this structure:
#     Title: [Title of the SaaS product];
#     Description: [Brief description of the product];
#     MRR: [Expected Monthly Recurring Revenue after 6 months];
#     Competitors: [List of direct competitors with country names];
#     Goods: [Key benefits];
#     Complexity: [Major technical complexities]."""
    
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#     ]
    
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=messages
#         )
#         ideas_text = response['choices'][0]['message']['content'].strip()
#         print("Debug - Raw ideas text:", ideas_text)

#         processed_ideas = parse_openai_response(ideas_text)

#         if processed_ideas:
#             return processed_ideas
#         else:
#             return [{'error': 'No valid ideas generated or incorrect format received'}]
#     except Exception as e:
#         print(f"Exception caught: {str(e)}")
#         return [{'error': str(e)}]




# @app.route('/generate', methods=['POST'], content_types=['application/json'])
# def generate_ideas():
#     request = app.current_request
#     body = request.json_body
    
#     category = body.get('category', 'general')
#     num_developers = body.get('num_developers', 1)
    
#     try:
#         generated_ideas = call_openai(category, num_developers)
#         if all('error' not in idea for idea in generated_ideas):
#             response_body = {'status': 'success'}
#             for index, idea in enumerate(generated_ideas, start=1):
#                 response_body[f'idea{index}'] = idea
#             return Response(body=response_body, status_code=200, headers={'Content-Type': 'application/json'})
#         else:
#             print("Error detected in ideas: ", generated_ideas)  # Debugging errors in ideas
#             return Response(body={'status': 'error', 'message': 'Failed to generate ideas or incorrect format received'}, status_code=404, headers={'Content-Type': 'application/json'})
#     except Exception as e:
#         print(f"Unhandled exception: {str(e)}")  # Debugging unhandled exceptions
#         return Response(body={'status': 'error', 'message': f"Error: {str(e)}"}, status_code=500, headers={'Content-Type': 'application/json'})
