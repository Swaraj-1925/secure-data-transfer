1)install node 

2)create a account on pinata and copy the api key and paste it after Bearer in app.py something like shown below
![image](https://github.com/Swaraj-1925/secure-data-transfer/assets/121567727/63cac507-f8b0-4598-b6cc-ee54bcba0058)


3) create a folder and open it in vs code
4) open a new terminal a new terminal and run:-  npm install --save-dev hardhat
5) after installing hardhat run npx hardhat -> create javascript with default configuration

6)then copy paste the Blockchain main folder and deploy.js file in your created folder

7)copy the content from uplod.sol and paste it in Lock.sol in contracts folder

8) copy the data from hardhat.config.js from this repo to the hardhat.config.js in your local computer

9) create a new terminal and run :- npx hardhat node   (dont close this terminal)

10)create a new terminal and run :- npx hardhat run --network localhost deploy.js

11)in your folder on your computer in client folder this is file Upload.json from that copy the abi part 

![image](https://github.com/Swaraj-1925/secure-data-transfer/assets/121567727/168c4dcd-eef3-4c16-b52a-4bf850b1d7fc)

12) replace the abi part in app.py in contract_abi part with you copied abi
13) after running  "npx hardhat run --network localhost deploy.js" you will gate a hash in treminal after  "Library deployed to: " copy that hash and replace contract_address
![image](https://github.com/Swaraj-1925/secure-data-transfer/assets/121567727/db1397b8-e307-4f29-beb4-715ce119c1e3)
15) run the python file
16) after opening the site you will have to enter priavte key from the terminal of (npx hardhat node) cammand and not  address

18) note that you can only use the address from  (npx hardhat node) terminal
![image](https://github.com/Swaraj-1925/secure-data-transfer/assets/121567727/088bd504-0b01-4868-9970-050661525bfd)

