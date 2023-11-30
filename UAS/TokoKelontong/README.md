# Grocery-Store

<h1 align="center">
<img align="center" height="80px" width="80px" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaDX9W6wWoAo3RNaRbfJfYCP0YSWLJqEqoFPPQuguOJpTjCDg8gpfOwjwHKsBlAs-ao27FrK_syLwZsniTwyZhGU-6RK5g=w2940-h1606" alt="Kai-icon">
 Kai
</h1>
<p align="center">
This is a grocery store desktop application for stock, customer, and cashier management.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#building-from-source">Building from source</a> •
  <a href="#support">Support</a> •
</p>

![image](https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaCeMYDQqt0b9GqwzbSDFg8uwproxSJWzAbK6TqIVN-Tp54Txw8VbPhOa31ACWCE1p5CLl_xv_G8BUCwkauPIz1FMh_B=w2940-h1606)

## Admin Menu

| Manage Pengguna                                                                                                                                                                           | Manage Barang                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="500" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaA0gLR4oCi5aB4FntnSAhS4i3ycjsKmudsMn8yAhdyNpF2fTvKn1Ebkn5d9QrKeg1IxrhBOFeCF2QxSssFlqLsd76yWrA=w2940-h1606"> | <img width="500" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaBh5NNCJiVSTI1Hyh2QXVDZtY1T66PV9e-c7MKDTQkKprX0T7gKRf9P0vuqVM0coSGXzXgG-w8FLlC3nUYH1mI8vS0mlg=w2940-h1606"> |

| Manage Supplier                                                                                                                                                                           | Manage Customer                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="500" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaDNmOR94W7Z-F9v8sBYyslpY7n-CpNcXwunAdkZ7g0qCtfGdMCCh-2Plae3D5NTb4Ku9G30x0BilHpEGjb_VJcF_Hj20g=w2940-h1606"> | <img width="500" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaAA3vwoMhOvKOnD2kyQ9W-ikMbXilEsg5ybbKmQ-JCgDdFu3FV8BGqYokSTCsC38seUPBX7aERtdzL-PKRj8x9CsqDFUA=w2940-h1606"> |

## Petugas Menu

| Grocery Store                                                                                                                                                                             | Cart                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="500" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaCFJz1wapt1AEQZsC0BP69uROigQIXVhkF-wsEYLZaDhjUPEPxejqHCTEoP5s04aKgd_brn5ZOLIfTyVTXgXgj8uk-rzA=w2940-h1606"> | <img width="500" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaBgx4UB1PwzhZJwQf5VOVryyWZQgKLiFM-DdtXw8j6UthBOfp7o4WTx68nmGqwCuqld17qfRKCPdGloapaTFRTrvJUH=w2940-h1606"> |

| Customer Area                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="500" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaA_m7wM_t6w1m-P8JXDGisd8EUGClzczRC2eP2kQ5wU3JGSsQQy-CebXOk-IabA9na35q3tMYoU56Y6QLtnsX1tKuXo_Q=w2940-h1606"> |

## Features

- Login
- Manage Barang
- Manage Pengguna
- Manage Barang
- Manage Supplier
- Manage Customer
- Manage Transaksi
- Manage Cart
- Manage Customer Area
- 2 Role (Admin dan Petugas)

1. **Admin**
   Username: admin
   Password: admin

2. **Petugas**
   Username: petugas
   Password: petugas

## Building from Source

Ensure you have [Python 3.12](https://www.python.org/downloads/) and [Git](https://github.com/git-guides/install-git) installed.

Open a terminal and run the following commands.

1. **Set everything up.**

- Linux/Mac

```
git clone https://github.com/iamwilldev/Grocery-Store && cd Grocery-Store && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

- Windows (Command Prompt)

```
git clone https://github.com/iamwilldev/Grocery-Store && cd Grocery-Store && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
```

2. **Build the app into an executable.**

```
pip install cx_freeze==6.15.10 && python main.py build
```

## Support

- You can support the development of Grocery-Store through donations on [GitHub Sponsors]().
- You can also leave a star on the github for more weebs to know about it.
- Grocery-Store is open to pull requests, so if you have ideas for improvements, feel free to contribute!
