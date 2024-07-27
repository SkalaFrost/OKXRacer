# OKX Race bot

- Automatically plays games by randomly choosing short or long
- Collects daily rewards
- Supports multiple accounts
- Works with a key, no authorization required
- Completes tasks
- Uses boost if there are no attempts left for the game

# Installation:
1. Install Python (Tested on 3.11)

2. Open cmd (terminal) and enter:
   ```
   git clone https://github.com/shinz1/OKXRacer.git
   ```
   
   ```
   cd OKXRacer
   ```
3. Install the modules:
   
   ```
   pip install -r requirements.txt
   ```

4. Run the script:
   ```
   python main.py
   ```

   or

   ```
   START.bat
   ```
   
## Insert the keys into the init_data file in the following format, each new key on a new line:
   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   ```
You may see `query_id=` or `user=`; there is no difference.

# How to get query_id:
Go to Telegram Web, open the bot, press F12 (or right-click and select "Inspect" in the desktop version), go to the Network tab, start the bot in the web version or reload the page in the desktop version, and look for a request with the name `tasks`. In the right column, find `query_id=xxxxxxxxxx` or `user=xxxxxxxxxx`.

# Support: [Tg channel](https://t.me/+oP6CHRAGQsI3Njdl)
