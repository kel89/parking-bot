FROM public.ecr.aws/lambda/python:3.11

# WebDriver Stuff --------------------------------------
# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
# RUN apt install -y wget xvfb unzip

# # Set up the Chrome PPA
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# # Update the package list and install chrome
# RUN apt update -y
# RUN apt install -y google-chrome-stable

# # Set up Chromedriver Environment variables
# ENV CHROMEDRIVER_VERSION 2.19
# ENV CHROMEDRIVER_DIR /chromedriver
# RUN mkdir $CHROMEDRIVER_DIR

# # Download and install Chromedriver
# RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
# RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# # Put Chromedriver into the PATH
# ENV PATH $CHROMEDRIVER_DIR:$PATH
# ------------------------------------------------------------

# Web Driver 2 -----------------------------------------------------------------
# Download chrome driver
RUN curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
RUN unzip chromedriver.zip
RUN rm chromedriver.zip

# Download Chrome Binary
RUN curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
RUN unzip headless-chromium.zip
RUN rm headless-chromium.zip

# Compress Driver and Binary
RUN zip -r chromedriver.zip chromedriver headless-chromium

#------------------------------------------------------------------------------

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]