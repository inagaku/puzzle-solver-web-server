import base64
import boto3
from image_processing import *
from puzzle_solver import *

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = "puzzle-queens"
    file_path = "queen_image.png"
    local_file_path = "/tmp/queen_image.png"

    try:
        s3.download_file(bucket_name, file_path, local_file_path)
        queen_img = cv2.imread(local_file_path, cv2.IMREAD_UNCHANGED)

        # Decode base64-encoded image from body
        image_data = event['body']
        img = cv2.imdecode(np.frombuffer(base64.b64decode(image_data), np.uint8), cv2.IMREAD_COLOR)

        cropped = crop_the_chess_board(img) # cropped colored image
        matrix = image_to_matrix(cropped) # 2D array where element is ((x, y), color)
        coordinates = solve_queens(matrix) # a list of coordinates (x, y)
        place_queens(cropped, coordinates, queen_img) # queens placed in "cropped" image

        # Encode back to JPEG
        _, buffer = cv2.imencode('.jpg', cropped)
        res_base64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/jpeg",
                "Access-Control-Allow-Origin": "*"
            },
            "isBase64Encoded": True,
            "body": res_base64
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error processing image: {str(e)}"
        }
