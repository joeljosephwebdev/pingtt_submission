# Submission for PingTT Project 📩

Thanks team for giving me the opportunity to work on this project! I had a lot of fun working on it, and encountered some unexpected challenges. Even so I believe I have a solution that produces the desired result.

## Authors 🙋‍♂️

- [Joel Joseph](https://www.github.com/joeljosephwebdev)

## Getting Started 💫

The project is really simple to execute. Just run solution.py
  ```sh
  python solution.py
  ```
The script takes about 10mins to fully complete so set it to run and grab yourself a cup of coffee. ☕

Once it's done you should see an output that looks like this.

  ```sh
    Complete!
    Identified 6893 employees.
    And it only took 654.6709158420563 seconds
  ```
A solution.json file will be generated in the same directory, containing all the records for employees believed to be slacking off and the events they may have attended. I included my solution.json output in the repo in case you run into any issues executing the script. You can delete it or leave it when you run your test, it should not matter.

### Prerequisites 🚀

The only Prerequisites are to have python3 anf the python requests library installed. I am specifically running Python 3.8.2. 

You will also need to download the attendance.json and employees.json files and add them to the directory.

* python version
   ```sh
    python3 --version  
    Python 3.8.2
   ```

* pip
  ```sh
  pip install requests
  ```
## Assumptions 🤔

I made a few assumptions while working on the project;

* Since it was not specified I assumed I could use any language for my solution.
* Even though I think we would have greatly benefited in terms of performance by converting the larger json files to database I assumed I should stick to json/mem since that it how the data was provided.
* Since it was not specified I assumed there was no grace period for leaving early.

## Wishlist 🌟

Here are some improvements I would have like to implement had I had more time;

* Implement multi-threading to split up the work on the attendance and employee dbs to allow for concurrent processing. This would have seen a drastic improvement to the speed of our program.
* Add basic error handling. (this would help with troubleshooting)
* Add logging. (this would help with troubleshooting)
* Setup script to accept args for different years or modifying grace period etc. (this would increase the versitility of the script and reduce the need to fidle in the future to run it for different parameters)
* Replace json loads with ijson iterations where possible. (While it would not help much with the speed of the script it would significantly reduce the amount of memory required to run)
