# Week 3 — Decentralised Authentication
This week we integrated Amazon Cognito into our backend application with a custom login page

## Why Cognito?
For web/mobile apps, Cognito provides
- Authentication: Log in to verify credentials
- Authorization: Manage access to services
- User Management: Allow the creation and management of a serverless user dbs

## User Pool
Used for user login/sign-up

## Identity Pool
Used to provide temporary AWS credentials to a user

![image](https://user-images.githubusercontent.com/67550608/227333457-aef535fb-388f-4ddd-9b97-f8cfdc4bd573.png)


## Authentication terms to remember
- SAML: Single-point or single-means of authentication to an application
- OpenID Connect: Using existing credentials (Instagram, LinkedIn etc.) to authenticate. **NOTE** it doesn't perform authorisation
- OAUTH: Usually used alongside openID Connect to authenticate credentials

# Instructions

## Configuring a User Pool
*****************************************

## Configuring Amplify

 Using the terminal go to the directory by typing the following command:
``` 
cd front-react-js 
npm i aws-amplyfy --save
```
this command will install amplify library and  will be added to the package.json

from the **app.js**, add the following codes:
```
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  //"aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_AWS_USER_POOLS_WEB_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});
```

from the **docker-compose.yml** on the frontend-react-js under environment:, add the following code
```
REACT_APP_AWS_PROJECT_REGION: "${AWS_DEFAULT_REGION}"
REACT_APP_AWS_COGNITO_REGION: "${AWS_DEFAULT_REGION}"
REACT_APP_AWS_USER_POOLS_ID: "${AWS_USER_POOLS_ID}"
REACT_APP_CLIENT_ID: "${APP_CLIENT_ID}"
```
Make sure to create the env var  **AWS_USER_POOLS_ID** and **APP_CLIENT_ID** on gitpod and codespace. (N.B: Since these env vars have not been loaded during the booting, you might get an error. either you rebuild your workspace or you pass the variable via the terminal. I do not hardcode the env vars for security reasons and for simplicity)
The AWS_USER_POOLS_ID and APP_CLIENT_ID you find when you configure the cognito user pool.


# Showing the components based on logged in/logged out

from the **homefeedpage.js** insert the following command
```
import { Auth } from 'aws-amplify';
```

this instruction is already implemented so you can skip this part
```
const [user, setUser] = React.useState(null);
```

delete the code with the  cookies 
```
  const checkAuth = async () => {
    console.log('checkAuth')
    // [TODO] Authentication
    if (Cookies.get('user.logged_in')) {
        display_name: Cookies.get('user.name'),
        handle: Cookies.get('user.username')
    }
  };
```

and replace with the following that used cognito
```
// check if we are authenticated
const checkAuth = async () => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};

```

this instruction is already implemented so you can skip this part
```
// check when the page loads if we are authenicated
React.useEffect(()=>{
  loadData();
  checkAuth();
}, [])
```

This instruction is already implemented so you can skip this part as well.
```
<DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
<DesktopSidebar user={user} />
```
On profileinfo.js, delete the following code
```
import Cookies from 'js-cookie'
```
and replace with the following
```
import { Auth } from 'aws-amplify';
```

remove the following code
```
    console.log('signOut')
    // [TODO] Authenication
    Cookies.remove('user.logged_in')
    //Cookies.remove('user.name')
    //Cookies.remove('user.username')
    //Cookies.remove('user.email')
    //Cookies.remove('user.password')
    //Cookies.remove('user.confirmation_code')
    window.location.href = "/"
```

and we replace with the new signout
```
const signOut = async () => {
    try {
        await Auth.signOut({ global: true });
        window.location.href = "/"
    } catch (error) {
        console.log('error signing out: ', error);
}
```

# Implementation of the sign in page
From the **signinpage.js** remove the following code
```
import Cookies from 'js-cookie'

```

and replace with the following
```
import { Auth } from 'aws-amplify';
```

remove the following code 
```
  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('')
    console.log('onsubmit')
    if (Cookies.get('user.email') === email && Cookies.get('user.password') === password){
      Cookies.set('user.logged_in', true)
      window.location.href = "/"
    } else {
      setErrors("Email and password is incorrect or account doesn't exist")
    }
    return false
  }
```
and replace it with the new one
```
const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();
    Auth.signIn(email, password)
    .then(user => {
      console.log('user',user)
      localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
      window.location.href = "/"
    })
    .catch(error => {
      if (error.code == 'UserNotConfirmedException') {
        window.location.href = "/confirm"
      }
      setErrors(error.message)
      });
    return false
  }
```

To try, just launch the container up on **"docker-compose.yml"**  and see if the login page works. to troubleshoot open "developer tools" or use inspect (browser) if you receive "NotAuthorizedException: Incorrect user or password".This means everything is set properly. if you got an error "auth not defined", the problem is the cognito user pool configuration. need to recreate.

Create a user on the cognito user pool and force change the password using the command on troubleshooting (there is no way to change on password via console). the password to login will be Testing1234! (as the commandline shows)

# Implement the signup page
Since you have managed to access using the credential created via console, it is time to delete it cos it is no anymore needed.

From the **signuppage.js** remove the following code
```
import Cookies from 'js-cookie'

```

and replace with the following
```
import { Auth } from 'aws-amplify';
```

delete the following command
```
  const onsubmit = async (event) => {
    event.preventDefault();
    console.log('SignupPage.onsubmit')
    // [TODO] Authenication
    Cookies.set('user.name', name)
    Cookies.set('user.username', username)
    Cookies.set('user.email', email)
    Cookies.set('user.password', password)
    Cookies.set('user.confirmation_code',1234)
    window.location.href = `/confirm?email=${email}`
    return false
  }
```

and add the new code
```
const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('')
    try {
      const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
          name: name,
          email: email,
          preferred_username: username,
        },
        autoSignIn: { // optional - enables auto sign in after user is confirmed
          enabled: true,
        }
      }) ;
      console.log(user);
      window.location.href = `/confirm?email=${email}`
    } catch (error) {
        console.log(error);
        setErrors(error.message)
    }
    return false
  }
```

# Implementation of the confirmation page
from the confirmationpage.js, remove the following code

 ```
import Cookies from 'js-cookie'

```

and replace with the following
```
import { Auth } from 'aws-amplify';
```

and remove the following code
```
  const resend_code = async (event) => {
    console.log('resend_code')
    // [TODO] Authentication
  }
```
and replace with the following
``` 
const resend_code = async (event) => {
 
    setErrors('')
    try {
      await Auth.resendSignUp(email);
      console.log('code resent successfully');
      setCodeSent(true)
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err)
      if (err.message == 'Username cannot be empty'){
        setCognitoErrors("You need to provide an email in order to send Resend Activation Code")   
      } else if (err.message == "Username/client id combination not found."){
        setCognitoErrors("Email is invalid or cannot be found.")   
      }
    }
  }

```

and remove the following code
```
 const onsubmit = async (event) => {
    event.preventDefault();
    console.log('ConfirmationPage.onsubmit')
    // [TODO] Authenication
    if (Cookies.get('user.email') === undefined || Cookies.get('user.email') === '' || Cookies.get('user.email') === null){
      setErrors("You need to provide an email in order to send Resend Activiation Code")   
    } else {
      if (Cookies.get('user.email') === email){
        if (Cookies.get('user.confirmation_code') === code){
          Cookies.set('user.logged_in',true)
          window.location.href = "/"
        } else {
          setErrors("Code is not valid")
        }
      } else {
        setErrors("Email is invalid or cannot be found.")   
      }
    }
    return false
  }
```

and replace with the cognito code
```
const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
    await Auth.confirmSignUp(email, code);
    window.location.href = "/"
  } catch (error) {
    setErrors(error.message)
  }
  return false
}
```

# Implementation of the recovery page
from the recoverpage.js, add the following code

 ```
import { Auth } from 'aws-amplify';
```

remove the following code
```
  const onsubmit_send_code = async (event) => {
    event.preventDefault();
    console.log('onsubmit_send_code')
    return false
  }
```

and add the these lines
```
const onsubmit_send_code = async (event) => {
    event.preventDefault();
    setErrors('')
    Auth.forgotPassword(username)
    .then((data) => setFormState('confirm_code') )
    .catch((err) => setErrors(err.message) );
    return false
  }
```

remove the following code
```
  const onsubmit_confirm_code = async (event) => {
    event.preventDefault();
    console.log('onsubmit_confirm_code')
    return false
  }
```

with the following new code
```
const onsubmit_confirm_code = async (event) => {
  event.preventDefault();
  setCognitoErrors('')
  if (password == passwordAgain){
    Auth.forgotPasswordSubmit(username, code, password)
    .then((data) => setFormState('success'))
    .catch((err) => setCognitoErrors(err.message) );
  } else {
    setCognitoErrors('Passwords do not match')
  }
  return false
}

```

## JWT Server Side Verification

In `HomeFeedPage.js` add the following header to pass along the access token
```
headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },

```



## Your Homepage should look similar to this
![image](https://user-images.githubusercontent.com/67550608/227733560-aa9a7a04-6714-4c9f-9bab-af5b40c16b63.png)

# tips
  
  ### Force a password change for a user created in Cognito

 aws cognito-idp admin-set-user-password --username nameofusername --password Testing1234! --user-pool-id "${AWS_USER_POOLS_ID}" --permanent







