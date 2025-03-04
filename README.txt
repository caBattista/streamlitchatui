pip install -r requirements.txt

# Put this into the optional sstartup command in azure app service configuration
python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0