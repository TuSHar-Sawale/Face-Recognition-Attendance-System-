from supabase import create_client

# Use the same URL and key as in your main.py
SUPABASE_URL = "https://ksfqvefeqhrnqutnkpxo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzZnF2ZWZlcWhybnF1dG5rcHhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc2Mzc0MjYsImV4cCI6MjA2MzIxMzQyNn0.nylC--UMAYovLgXa5BsxHwY9_8i4Pa9C6xZ7H8bOYDU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_student_image(supabase, student_id, default_size=(216, 216)):
    """
    Retrieves student image from Supabase storage with better error handling
    """
    try:
        # First check if the image exists
        files = supabase.storage.from_("student-images").list()
        file_exists = any(f"{student_id}.png" in file['name'] for file in files)

        if not file_exists:
            print(f"Image file for student {student_id} does not exist in storage")
            return create_default_image(default_size)

        # Try to download the image
        response = supabase.storage.from_("student-images").download(f"{student_id}.png")
        if response is None:
            print(f"Failed to download image for student {student_id}")
            return create_default_image(default_size)

        # Convert image data to numpy array
        nparr = np.frombuffer(response, np.uint8)
        img = cv2.imdecode(nparr, cv2.COLOR_BGRA2BGR)

        if img is None:
            print(f"Failed to decode image for student {student_id}")
            return create_default_image(default_size)

        return img

    except Exception as e:
        print(f"Error loading image for student {student_id}: {str(e)}")
        return create_default_image(default_size)


def create_default_image(size=(216, 216)):
    """
    Creates a default image with student placeholder
    """
    img = np.zeros((size[0], size[1], 3), np.uint8)
    # Add a placeholder text
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "No Photo"
    textsize = cv2.getTextSize(text, font, 1, 2)[0]

    # Get coords based on boundary
    textX = (img.shape[1] - textsize[0]) // 2
    textY = (img.shape[0] + textsize[1]) // 2

    # Add text centered on image
    cv2.putText(img, text, (textX, textY), font, 1, (255, 255, 255), 2)
    return img