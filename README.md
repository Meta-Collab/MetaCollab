<h1>MetaCollab</h1>
<p align="center">
</p>

<a href="https://hack36.com"> <img src="https://i.postimg.cc/FFwvfkGk/built-at-hack36.png" height=24px> </a>

- ### <a href="https://youtu.be/XTADBtRyZK8">Demo Video </a>
- ###  <a href="https://docs.google.com/presentation/d/1xnV0S1DYB7M-MCk9P0KP_HKoeN-4uKUMm_g0N1yy62c/edit?usp=sharing"> PPT link </a>

## Introduction:
  Tracking users' daily activities on their smartphones and other devices, often shared with companies, raises serious concerns about data privacy. Such practices compromise users' privacy and put their data at risk of misuse and unauthorized access, including being sold to third-party apps. For instance, ubiquitous features like keyboard word prediction and fitness activity tracking, designed to enhance user experience, inadvertently become conduits for extensive data collection, leaving users vulnerable to exploitation.

## How do we solve the Problem?
Rather than directly sharing data across devices to train a model for generating recommendations, we address this challenge by distributing a pre-trained model and a numpy array containing the resulting weights of model training across a network of users' diverse devices via blockchain technology. When a device's collected data is required to contribute to training the distributed model, we train its model locally on its own dataset and aggregate its resultant weights with the weights already stored on blockchain using the pre-trained model stored in IPFS, using federated learning techniques. Subsequently, we update the numpy array on the blockchain, whereas the pre-trained model remains the same. This methodology enhances privacy and security while promoting improvement in the collaborative model.
  
## Demo
![WhatsApp Image 2024-04-21 at 9 43 43 AM](https://github.com/Meta-Collab/MetaCollab/assets/31176772/c637d862-fa83-4086-bd00-2d8777ed6aef)

![WhatsApp Image 2024-04-21 at 9 43 46 AM](https://github.com/Meta-Collab/MetaCollab/assets/31176772/b73d142a-0a13-45a0-a588-c06a8fe220e7)

![WhatsApp Image 2024-04-21 at 9 52 39 AM](https://github.com/Meta-Collab/MetaCollab/assets/31176772/0d8e7090-484f-4cb3-9e23-6ea778463fec)

![WhatsApp Image 2024-04-21 at 10 21 55 AM](https://github.com/Meta-Collab/MetaCollab/assets/31176772/1fa413ff-c534-4918-b67d-815b10317fd3)

![WhatsApp Image 2024-04-21 at 10 25 10 AM](https://github.com/Meta-Collab/MetaCollab/assets/31176772/fd76539e-c124-42a2-93d5-8660ce5eeb20)


## Technology Stack: 
  1) Hardhat
  2) Solidity
  3) IPFS
  4) Ethereum
  5) Django
  6) Node.js
  7) Federated Learning
  8) LSTM
  9) Metamask
  10) JavaScript

  
## Contributors:

Team Name: AIOverlords

* [Eleena Sarah Mathew](https://github.com/eleensmathew/)
* [Nandika Agrawal](https://github.com/Nandika-A)
* [Manan Arora](https://github.com/Manan-Arora31)
* [Ritesh Kumar Maurya](https://github.com/MauryaRitesh)

## Challenges We Faced
1. Integrating blockchain and machine learning technologies proved time-consuming, necessitating the use of Django to interface with ML and Node.js to interface with Hardhat. Bridging these disparate web technologies posed complexities that we addressed through Axios. 
2. Optimizing gas fees in smart contracts presented a formidable hurdle. We underwent multiple iterations of optimization to minimize gas usage. 
3. Implementing federated learning techniques also posed considerable challenges, demanding thorough attention to detail and innovative problem-solving.


### Made at:
<a href="https://hack36.com"> <img src="https://i.postimg.cc/FFwvfkGk/built-at-hack36.png" height=24px> </a>
