import cv2
import numpy as np

def apply_pixel_grid(image_path, pixel_size):
    # 画像をグレースケールで読み込む
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 2値化処理を適用する
    _, binary_image = cv2.threshold(image, 199, 255, cv2.THRESH_BINARY)

    # 元の画像のサイズを方眼紙のピクセルサイズで整数倍に切り捨てる
    resized_width = (binary_image.shape[1] // pixel_size) * pixel_size
    resized_height = (binary_image.shape[0] // pixel_size) * pixel_size
    binary_image = binary_image[:resized_height, :resized_width]

    # 方眼紙のピクセルサイズで画像を分割し、各領域内に画素値が存在するかをチェックする
    result = np.zeros((binary_image.shape[0] // pixel_size, binary_image.shape[1] // pixel_size), dtype=np.uint8)
    for y in range(0, binary_image.shape[0], pixel_size):
        for x in range(0, binary_image.shape[1], pixel_size):
            pixel_area = binary_image[y:y+pixel_size, x:x+pixel_size]
            if np.sum(pixel_area ==  0):  # 方眼内に黒が存在する場合
                result[y // pixel_size, x // pixel_size] = 0  # 黒に設定
            else:
                result[y // pixel_size, x // pixel_size] = 255  # 白に設定
    # 結果のピクセル画像を作成する
    result_image = np.repeat(np.repeat(result, pixel_size, axis=0), pixel_size, axis=1)

    return result_image

# 使用例
pixel_size = 10  # 方眼紙のピクセルサイズ
image_path = 'sample3.jpg'  # 入力画像のパス
result_image = apply_pixel_grid(image_path, pixel_size)

cv2.imshow('Result', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
