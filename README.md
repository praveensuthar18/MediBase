# Setup Instructions

Use a Linux Based PC or a Macbook to run the following steps

1. Navigate to the `CODE` directory.
   
    ```bash
    cd CODE
    ```

2. Install the required Python packages from `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

3. Move into the `server_code` directory.

    ```bash
    cd server_code
    ```

4. Download the metamap ZIP file from the following link:

    [Download metamaplite.zip](https://drive.google.com/file/d/18Pws0FwjUn-SGvIGh4CYxY-_pWuFvChQ/view?usp=sharing)

5. Unzip the `metamaplite.zip` file.

6. Download the solr-config ZIP file from follwing link :
    [Download solr-config.zip](https://drive.google.com/file/d/1g8xNVoIH-ioJFv79CZMasnW9wver4ERA/view?usp=sharing)

7. Unzip the `solr-config.zip` filr.

8. Navigate into the `solr-config` directory.

    ```bash
    cd solr-config
    ```

9. Start the Solr server on port 8983.

    ```bash
    bin/solr start -p 8983
    ```

10. Create a core 'healthify' in the Apache solr to upload documents.

    ```bash
    bin/solr create -c healthify
    ```

11. Go back to the previous directory.

    ```bash
    cd ..
    ```

12. Download the `processed_medical_data.json` file from the following link:

    [Download processed_medical_data.json](https://drive.google.com/file/d/1_EZip3zQlM1Ie0fWak2X716AQW_7HPMw/view?usp=sharing)

13. Upload the `merged_data.json` file to Solr.

    ```bash
    curl 'http://localhost:8983/solr/healthify/update?commit=true' --data-binary @processed_medical_data.json -H 'Content-type:application/json'
    ```

14. Run the `app.py` script.

15. Go back to the parent directory.

    ```bash
    cd ..
    ```

16. Move into the `front_end` directory.

    ```bash
    cd front_end
    ```

17. Start a simple HTTP server.

    ```bash
    python -m http.server
    ```

18. Open the web page in your browser at the following address:

    [http://localhost:8000/](http://localhost:8000/)
