import os
import shutil
from pathlib import Path
import fitz

currentPath = os.path.dirname(os.path.abspath(__file__))
sourcePath = currentPath + '\\source'
resultPath = currentPath + '\\result'

shutil.rmtree(resultPath, ignore_errors=True, onerror=None)  # Clear result dir

print('Экстрактор нечетных страниц для PDF квитанций')
print('\n')
print('\n\n')

fileCounter = 0
sourcePdfFolderCounter = os.walk(sourcePath)  # Get directory iterator & counter
for root, directories, filenames in sourcePdfFolderCounter:
    for filename in filenames:
        pdf_source_file_path_counter = os.path.join(root, filename)
        if Path(pdf_source_file_path_counter).suffix == '.pdf':
            fileCounter += 1

fileCounterCycle = 0
sourcePdfFolder = os.walk(sourcePath)  # Get directory iterator & main cycle
for root, directories, filenames in sourcePdfFolder:
    for filename in filenames:
        pdf_source_file_path = os.path.join(root, filename)
        if Path(pdf_source_file_path).suffix == '.pdf':
            pdf_source_processing = fitz.open(pdf_source_file_path)  # open source pdf file for processing

            pdf_dest_dir = resultPath \
                           + root.partition(sourcePath)[2]
            Path(pdf_dest_dir).mkdir(parents=True, exist_ok=True)  # making dest dir

            p_odd = []  # Get odd pages
            for page_number in range(pdf_source_processing.pageCount):
                if page_number % 2 == 0:
                    p_odd.append(page_number)

            pdf_source_processing.select(p_odd)  # extract odd pages
            pdf_dest_path = pdf_dest_dir + '\\' + filename

            pdf_source_processing.save(pdf_dest_path, garbage=3)  # save
            pdf_source_processing.close()

            fileCounterCycle += 1
            completePercent = 100 * fileCounterCycle / fileCounter
            print("Готовность: %.0f" % completePercent + '%')

print('\n')
print('Готово, результат в папке result')
print('\n')
os.system('pause')
