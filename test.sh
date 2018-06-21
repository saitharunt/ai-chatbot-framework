find / -name "/usr/src/app/training_data"
if [ $(echo $?) -ne 0 ]; then
    cp /Users/vn0o7tt/ai-chatbot-framework/app/training_data /usr/src/app/training_data
fi