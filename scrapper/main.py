from datetime import datetime
import pathlib
import functools
import mechanicalsoup as msoup
import wget

today = datetime.today()
targetPathStr = "F:/tmp_data"
url = "https://www.google.com/imghp?hl=en"
searchTerm = "cat"
totalImagesRequired = 100
targetPath = pathlib.Path(f"{targetPathStr}/{today.strftime('%Y%m%d_%H%M%S')}_{searchTerm}")

browser = msoup.StatefulBrowser()
browser.open(url)
print(browser.get_url())

# Get HTML
browser.get_current_page()

# Search the search input form
browser.select_form()
browser.get_current_form()

# Search for the term
browser["q"] = searchTerm

# Submit the form
# browser.launch_browser()
response = browser.submit_selected()

print("New URL: ", browser.get_url())
print("My response ...\n", response.text[:500])

# Open new URL
newUrl = browser.get_url()
browser.open(newUrl)

# Get HTML
resultPage = browser.get_current_page()
imagesTags = resultPage.find_all("img")

imageUrls = []
for image in imagesTags:
    image = image.get("src")
    imageUrls.append(image)

imageUrls = [image for image in imageUrls if image.startswith("https")]

targetPath.mkdir(parents=True, exist_ok=True)

# Downloading the images
numWidth = len(str(totalImagesRequired))
counter = 1
for image in imageUrls:
    # fileName = f"{searchTerm}_{counter:0={numWidth}}_{pathlib.Path(image).name}"
    fileName = f"{searchTerm}_{counter:0={numWidth}}.jpg"
    targetFilePath = targetPath.joinpath(fileName)

    wget.download(url=image, out=targetFilePath.as_posix())
    counter += 1
    if counter > totalImagesRequired:
        break
