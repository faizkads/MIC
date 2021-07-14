from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

import tkinter as tk

ENDPOINT = "https://which-gamelan.cognitiveservices.azure.com/"

training_key = "a1eed5464ec84f04a5fcbdc7d083c45d"
prediction_key = "ef4ca5e9ed3a4053b768a6d0507d6105"
prediction_resource_id = "/subscriptions/b4786abb-baa4-44aa-b6bc-df83b5d9f721/resourceGroups/Imagine/providers/Microsoft.CognitiveServices/accounts/whichgamelan-Prediction"
publish_iteration_name = "classifyModel"

# Now there is a trained endpoint that can be used to make a prediction
training_credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, training_credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Get the project with specified name from Azure
project = next(filter(lambda p: p.name == "Classify Gamelan", trainer.get_projects()), None)
if not project:
    print ("Couldn't find project")
    exit(-1)

def get_info(tag):
    if (tag=="Bonang"):
        information = "-Keluarga “Pencon”, tempat pukulan cembung di logam. \n -Ditabuh dengan 2 pemukul khusus berbalut kain.\n -Teknik Pipilan :  menjadi penuntun lagu dengan melodi bersinambungan. \n -Teknik Imbalan : menggunakan melodi jalin-menjalin dengan bonang lainnya. \n -Khusus : Sekaran, adalah lagu hiasan yang dapat ditambahkan dalam lagu."
    elif (tag=="Demung"):
        information = "-Keluarga “Balungan”, berupa bilahan logam bernilai 1 oktaf setiap bilahnya. \n -Ditabuh dengan sebuah pemukul berbentuk palu.\n -Dimainkan dengan melodi mengikuti lagu.\n -Teknik ‘memathet’ yaitu memencet bilahan setelah dipukul agar tidak berdengung."
    elif (tag=="Gender"):
        information ="-Keluarga “Balungan”, berupa bilahan logam bernilai 1 oktaf setiap bilahnya.\n -Ditabuh dengan pemukul berlilit kain.\n -Sebagai melodi pengisi lagu"
    elif (tag=="Gong"):
        information ="-Keluarga “Pencon”, yang paling besar, digantung di peranti kayu.\n -Untuk menandai perubahan tempo dan dinamik, dengan suara besar nya\n -Menegaskan irama tertentu dalam lagu untuk suasana."
    elif (tag=="Kendang"):
        information ="-Instrumen tabung dibalut kulit kerbau dan kambing untuk suara yang berbeda.\n -Ditabuh dengan menggunakan telapak tangan.\n -Berfungsi sebagai pengatur irama dan pembuka lagu."
    elif (tag=="Kenong"):
        information ="-Keluarga “Pencon”, tempat pukulan cembung di logam.\n -Ditabuh dengan 2 pemukul khusus berbalut kain.\n -Pengisi akor/harmoni, menegaskan batas ‘gatra’ dan irama."
    elif (tag=="Rebab"):
        information ="-Biola budaya Asia dan Timur Tengah.\n -Berbentuk tegak, terdiri dari 3 senar dengan nada yang terbatas.\n -Dimainkan dengan di gesek menggunakan busur.\n -di beberapa daerah digunakan dalam ritual penyembuhan."
    elif (tag=="Siter"):
        information ="-Gitar Jawa yang hampir punah\n -Alat musik petikan yang terdiri dari 14 buah senar\n -Terdapat 2 sisi yang dapat dimainkan untuk menghasilkan suara yang berbeda"
    else:
        information = " No information."
    return information


# Create main window
window = tk.Tk()
window.lift()
window.attributes("-topmost", True)
window.title("Gamelan Predictor")
window['background']='#dbd68e'

# Create the input field for image url
url_frame = tk.Frame(window)
url_frame.pack()
url_label = tk.Label(url_frame, text="Image Url")
url_label.pack( side = tk.LEFT)
url_entry = tk.Entry(url_frame, width=60)
url_entry.pack(side = tk.RIGHT)

prediction_text = tk.Text(window,height=10, width=90)
prediction_text.insert(tk.INSERT, "Gamelan Name:\n")
prediction_text.insert(tk.INSERT, "Brief info:\n")
prediction_text.config(state=tk.DISABLED)  # make readonly

# function to show prediction after button is pressed
def predict():
  try:
    results = predictor.classify_image_url(project.id,publish_iteration_name,url=url_entry.get())
    for prediction in results.predictions:
      if prediction.probability > 0.5 :
        prediction_text.config(state=tk.NORMAL) # allow edit to show result
        prediction_text.delete('1.0', tk.END) # clear textarea
        prediction_text.insert(tk.INSERT, "\nGamelan Name: " + prediction.tag_name + " ({0:.2f}%)".format(prediction.probability * 100) + "\n")
        prediction_text.insert(tk.INSERT, "Brief info:\n " + get_info(prediction.tag_name))
        prediction_text.config(state=tk.DISABLED)  # make readonly again
        break 
  except:
    # show "Invalid URL"
    prediction_text.config(state=tk.NORMAL) # allow edit to show result
    prediction_text.delete('1.0', tk.END) # clear textarea
    prediction_text.insert(tk.INSERT, "Invalid URL")
    prediction_text.config(state=tk.DISABLED)  # make readonly again

  url_entry.delete(0, tk.END) # clear url

# create the button
predict_btn = tk.Button(window, text="Analyze Image", command=predict,height=2, width=40)
predict_btn.pack()

# pack the prediction result text after the button
prediction_text.pack()

# show the window
window.mainloop()
