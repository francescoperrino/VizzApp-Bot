# VizzApp-Bot

## Installazione

1.  **Ambiente Virtuale**: È consigliato utilizzare un ambiente virtuale per isolare le dipendenze del progetto. Esegui il seguente comando per creare un ambiente virtuale:

    ```bash
    $ python3 -m venv .venv
    ```

2.  **Attivazione dell'Ambiente Virtuale**: Attiva l'ambiente virtuale per garantire che le dipendenze del progetto siano installate in modo isolato. A seconda del sistema operativo, usa il comando appropriato:

    - Su Linux/MacOS:

      ```bash
      $ source venv/bin/activate
      ```

    - Su Windows:

      ```bash
      $ .\venv\Scripts\activate
      ```

3.  **Installazione delle Dipendenze**: Ora installa i pacchetti necessari eseguendo il seguente comando:

    ```bash
    $ pip install -r requirements.txt
    ```

## Configurazione del Bot

Prima di poter avviare il bot, è necessario crearne uno nuovo su Telegram e configurarlo correttamente. Segui questi passaggi:

1.  **Creazione di un Nuovo Bot Telegram**:

    - Avvia una chat con [@BotFather](https://t.me/botfather).
    - Utilizza il comando `/newbot` e segui le istruzioni per creare un nuovo bot.
    - Dopo aver completato la creazione, riceverai un `BOT_USERNAME` e un `BOT_TOKEN` che serviranno per configurare il bot.
    - Nella chat con [@BotFather](https://t.me/botfather), utilizza il comando `/setcommands` per configurare i comandi del bot. Puoi usare l'esempio seguente:

      ```
      frase - Frase random o specifica (/frase numero).
      tutte_frasi - Elenco di tutte le frasi.
      ```

2.  **Configurazione delle Variabili d'Ambiente**:

    - Crea un file denominato `.env` nella directory del progetto.
    - All'interno del file `.env`, definisci le seguenti variabili sostituendo i valori appropriati:

      ```python
      BOT_USERNAME = '@username_bot'
      BOT_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
      ```

3.  **Configurazione Firebase**:

    3.1. **Creazione di un Progetto Firebase:**

    - Vai alla [console di Firebase](https://console.firebase.google.com/) e crea un nuovo progetto.
    - Segui le istruzioni per dare un nome al tuo progetto e configurare le impostazioni necessarie.

      3.2. **Configurazione del Database Firestore:**

    - Nel menu a sinistra, seleziona "Firestore Database".
    - Clicca su "Crea database".
    - Scegli la modalità "Produzione" o "Test" in base alle tue esigenze.
    - Seleziona la regione più vicina a te.
    - Clicca su "Avanti" e poi su "Attiva".

      3.3. **Aggiunta di Dati al Database:**

    - Crea una nuova "Collezione" (ad esempio, "sentencesCollection").
    - Aggiungi documenti alla collezione, dove ogni documento rappresenta un dato.
    - Ogni documento può contenere campi di vario tipo (stringhe, numeri, array, ecc.).
    - **Importante:** Assicurati che ogni documento nella collezione `sentencesCollection` contenga un campo chiamato `sentences` che è un array di stringhe.

      3.4. **Configurazione delle Regole di Sicurezza:**

    - Nella scheda "Regole" del database Firestore, definisci le seguenti regole di sicurezza per controllare l'accesso ai tuoi dati:

      ```
      rules_version = '2';
      service cloud.firestore {
        match /databases/{database}/documents {
          match /{document=**} {
            allow read, write: if false;
          }
          match /sentencesCollection/{sentencesArray} {
            allow read: if true;
            allow create, update: if request.auth != null;
            allow delete: if false;
          }
        }
      }
      ```

    - Queste regole consentono a chiunque di leggere i documenti nella collezione `sentencesCollection`, ma richiedono l'autenticazione per la creazione e l'aggiornamento.

      3.5. **Ottenimento del File di Credenziali:**

    - Nella console di progetto di Firebase, vai in impostazioni progetto -> account di servizio -> genera nuova chiave privata.
    - Questo genererà un file JSON, che conterrà le credenziali per connettere il tuo codice al database.

## Avvio del Bot

Una volta configurato l'ambiente e il bot, puoi avviare il bot eseguendo il seguente comando:

```bash
$ python3 vizzapp.py
```
