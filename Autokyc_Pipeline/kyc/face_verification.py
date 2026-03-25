from deepface import DeepFace

def verify_face(id_image_path, selfie_path):
    try:
        result = DeepFace.verify(
            img1_path=id_image_path,
            img2_path=selfie_path,
            enforce_detection=False
        )

        return {
            "verified": result["verified"],
            "distance": result["distance"]
        }

    except Exception as e:
        return {
            "verified": False,
            "error": str(e)
        }