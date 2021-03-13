#!/bin/bash
tensorflow_model_server \
  --rest_api_port=9000 \
  --model_name=emoModel \
  --model_base_path=/var/www/Portfolio/WebApp/essentials/FER
