import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize the S3 client
s3 = boto3.client('s3')

def create_bucket(bucket_name, region="us-east-1"):
    """Create an S3 bucket in a specified region."""
    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating bucket: {e}")

def upload_file(bucket_name, file_name, object_name=None):
    """Upload a file to an S3 bucket."""
    object_name = object_name or file_name
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"File '{file_name}' uploaded as '{object_name}' to bucket '{bucket_name}'.")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error uploading file: {e}")

def list_files(bucket_name):
    """List files in an S3 bucket."""
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            print("Files in bucket:")
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print("Bucket is empty.")
    except Exception as e:
        print(f"Error listing files: {e}")

def download_file(bucket_name, object_name, file_name):
    """Download a file from an S3 bucket."""
    try:
        s3.download_file(bucket_name, object_name, file_name)
        print(f"File '{object_name}' downloaded from bucket '{bucket_name}' to '{file_name}'.")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error downloading file: {e}")

def delete_file(bucket_name, object_name):
    """Delete a file from an S3 bucket."""
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"File '{object_name}' deleted from bucket '{bucket_name}'.")
    except Exception as e:
        print(f"Error deleting file: {e}")

# Main function for testing
if __name__ == "__main__":
    bucket_name = input("Enter bucket name: ").strip()
    region = input("Enter region (default 'us-east-1'): ").strip() or "us-east-1"
    
    # 1. Create a bucket
    create_bucket(bucket_name, region)

    while True:
        print("\nOptions:")
        print("1. Upload File")
        print("2. List Files")
        print("3. Download File")
        print("4. Delete File")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            file_name = input("Enter file path to upload: ").strip()
            object_name = input("Enter S3 object name (or press Enter to use file name): ").strip()
            upload_file(bucket_name, file_name, object_name)
        elif choice == "2":
            list_files(bucket_name)
        elif choice == "3":
            object_name = input("Enter the object name to download: ").strip()
            file_name = input("Enter the local file name to save as: ").strip()
            download_file(bucket_name, object_name, file_name)
        elif choice == "4":
            object_name = input("Enter the object name to delete: ").strip()
            delete_file(bucket_name, object_name)
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")
