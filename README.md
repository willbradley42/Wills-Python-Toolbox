# Will's Python Toolbox
A collection of random/useful scripts, created in Python.
All of these tools are simple to run, just navigate to the directory containing the scripts and then:

`bash
python3 <toolname>.py
`

# Tools
This list will (hopefully) get bigger as time goes on, as I come up with new ideas.

## fileorganiser.py

Sorts all files in a directory into subdirectories, based on the extension. Current support for:

<ul>
  <li>Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg, .heic</li>
  <li>Documents: .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx</li>
  <li>Videos: .mp4, .mov, .avi, .mkv, .wmv, .flv, .webm</li>
  <li>Audio: .mp3, .wav, .aac, .ogg, .flac, .m4a</li>
  <li>Archives: .zip, .rar, .tar, .gz, .7z</li>
  <li>Executables: .exe, .msi, .bat, .sh</li>
  <li>Scripts: .py, .js, .html, .css, .php, .java, .c, .cpp</li>
  <li>Presentations: .ppt, .pptx, .key, .odp</li>
  <li>Spreadsheets: .xls, .xlsx, .ods, .csv</li>
  <li>Text Docs: .txt, .md, .log</li>
</ul>

Any extensions not listed above are in the "Other" category, and will be placed in a subdirectory called "Others".


## watermarker.py

Dependencies: Pillow

This generates a watermark over a provided image. The watermark can be text, or another image. Support for different fonts, as long as they are installed.

