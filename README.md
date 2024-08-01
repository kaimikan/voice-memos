# voice-memos

A small app with a keyboard-activatable voice recording which then gets transcribed and saved as text a memo.

# **Setup**

1. Install the following libraries:

   ```
   pip install keyboard, pyaudio, pocketsphinx
   ```
2. Files needed for voice transcription (disclaimer: the results are not very accurate, since [PocketSphinx](https://github.com/cmusphinx/pocketsphinx) is quite an old project at this point, so you can just run it without the files and without transriptions):

   * [cmudict-en-us](https://github.com/cmusphinx/pocketsphinx/blob/master/model/en-us/cmudict-en-us.dict)
   * [cmusphinx-en-us-5.2](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English/cmusphinx-en-us-5.2.tar.gz/download)
