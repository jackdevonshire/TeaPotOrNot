# Tea Pot Or Not?

As the name suggests, this is an API to determine if an image is a teapot or not...

## Usage
This API follows the RFC 2324 Hyper Text Coffee Pot Protocol, otherwise known as HTCPCP/1.0 (https://www.rfc-editor.org/rfc/rfc2324).

Once launched, you should send a BREW request to the /brew endpoint. POST does work, but really you should be using a BREW request. Under normal circumstances, the request content type should be `application/coffee-pot-command` however as we need to send an image to the server,
please set the content type to `multipart/formdata`


```curl
curl --request BREW \
  --url http://127.0.0.1:5000/brew \
  --header 'Content-Type: multipart/form-data' \
  --form 'file=@C:\path\to\image.png'
```


### Success Responses
When file is a picture of a teapot
```javascript
    HTCPCP/1.0 418
    Content-Type: application/json
    {'HasError': false, 'Message': 'I'm a teapot'}
```
When file is a picture of a coffee machine
```javascript
    HTCPCP/1.0 200
    Content-Type: application/json
    {'HasError': false, 'Message': 'Here's your coffee! ☕'}
```
When file is not a teapot or a coffee machine
```javascript
    HTCPCP/1.0 200
    Content-Type: application/json
    {'HasError': false, 'Message': 'I'm not a teapot'}
```

### Error Responses
When no files are provided
```javascript
    HTCPCP/1.0 400
    Content-Type: application/json
    {'HasError': true, 'Message': 'No file provided'}
```
When file is not in the correct format
```javascript
    HTCPCP/1.0 400
    Content-Type: application/json
    {'HasError': true, 'Message': 'File type must be png, jpg or jpeg'}
```

## Why?
I recently remembered that this easter egg existed, and I decided to look a bit more into it's history... I then landed upon two Github issues with a request to remove the 418 status code from both the Node and Go languages, which rightfully where met with a vicious defence. The only thing people on those issues could complain about was the fact that the code itself is "useless" and takes up valuable space. Hopefully this project will prove that 418 is not a useless status code after all.

I'm also doing this to learn more about machine learning.
