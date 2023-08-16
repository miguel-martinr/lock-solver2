import cv2
import pytesseract


def imshow(image, name='image'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_rectangle(top_left, bottom_right):
    # Get the rectangle coordinates
    x = top_left[0]
    y = top_left[1]
    w = bottom_right[0] - top_left[0]
    h = bottom_right[1] - top_left[1]

    # Return the rectangle coordinates
    return (x, y, w, h)


def get_text_from_image_at_rectangle(
        image,
        rectangle,
        whitelist=None
):

    # Get the rectangle coordinates
    x, y, w, h = get_rectangle(rectangle[0], rectangle[1])

    # Crop the image to the rectangle coordinates
    cropped_image = image[y:y+h, x:x+w]

    # Convert the cropped image to grayscale
    grayscale_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Upsample the cropped image
    grayscale_image = cv2.resize(
        grayscale_image,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC 
    )


    # # Apply adaptive thresholding to the grayscale image
    _, thresholded_image = cv2.threshold(
        grayscale_image,
        120,
        255,
        cv2.THRESH_BINARY
    )

    # Remove noise
    thresholded_image = cv2.medianBlur(thresholded_image, 5)  # El valor "5" es el tamaño del kernel (debe ser un número impar)
    
    # Erode the image
    # kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (3, 3))
    # thresholded_image = cv2.erode(thresholded_image, kernel, iterations=1)

    # _, thresholded_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Bitwise-not the thresholded image
    thresholded_image = cv2.bitwise_not(thresholded_image)

    # Expand white background
    thresholded_image = cv2.copyMakeBorder(
        thresholded_image,
        30,
        30,
        30,
        30,
        cv2.BORDER_CONSTANT,
        value=(255, 255, 255)
    )

    # Creaete black border
    # thresholded_image = cv2.copyMakeBorder(
    #     thresholded_image,
    #     10,
    #     10,
    #     10,
    #     10,
    #     cv2.BORDER_CONSTANT,
    #     value=(0, 0, 0)
    # )

    # imshow(thresholded_image, 'bitwisenot')


    # Add white border to the thresholded image
    # thresholded_image = cv2.copyMakeBorder(
    #     thresholded_image,
    #     10,
    #     10,
    #     10,
    #     10,
    #     cv2.BORDER_CONSTANT,
    #     value=(0, 0, 0)
    # )

    # imshow(thresholded_image, 'border')




    config =""
    # psm 11 = Sparse text. Find as much text as possible in no particular order.
    # oem 3 = Default OCR Engine modes
    config += "--psm 7 --oem 3"

    # Whitelist
    if whitelist:
        config += " -c tessedit_char_whitelist=" + whitelist
  
    # Line separator
    config += " -c page_separator=''"        
        
    imshow(thresholded_image, 'thresholded_image')
    text = pytesseract.image_to_string(
        thresholded_image, config=config)

    print(text)

    # Return the text
    return str(text.replace('\n', ''))
