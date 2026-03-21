from app.extensions import render_template,redirect,flash,url_for,abort,request,g,session,db,jsonify,CURR_USER_KEY,os,APP_STATIC,EMAIL_RESET,Send_Email,URLSafeTimedSerializer,SignatureExpired,BadTimeSignature,google_client_config
from app.auth import bp
from app.forms.auth.login import LoginForm
from app.forms.auth.register import RegisterForm
from app.models.users import User
from google_auth_oauthlib.flow import Flow
import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token
import requests


flow = Flow.from_client_config(
    client_config=google_client_config,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=f"{os.getenv('GOOGLE_REDIRECT_URI_BASE',None)}/auth/google/callback"
)

serializer = URLSafeTimedSerializer(os.getenv('URL_SAFE_KEY',None))


@bp.route('/google-login')
def google_login():
    flow.prompt = 'select_account'
    authorization_url, state = flow.authorization_url(prompt='select_account')
    session["state"] = state
    return redirect(authorization_url)

@bp.route('/google/callback')
def google_login_callback():

    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience= os.getenv('GOOGLE_CLIENT_ID',None)
    )
    user = User.get_users().filter(User.oauth_uid == id_info.get("sub"), User.is_active == True, User.is_oauth == True).first()
    if user:

        user.first_name = id_info.get("given_name")
        user.last_name = id_info.get("family_name")
        user.email = id_info.get("email")
        user.oauth_provider = "Google"
        user.oauth_uid = id_info.get("sub")
        user.oauth_profile_url = id_info.get("picture")
        db.session.add(user)
        db.session.commit()

        session[CURR_USER_KEY] = user.id
        flash('Successfully authenticated!','success')
        return redirect(url_for('main.index'))
    else:
        user = User.get_users().filter(User.email == id_info.get("email"),User.is_oauth == False).first()
        if user:
            flash('This email address already exists!','warning')
            return redirect(url_for('auth.authentication'))

        first_name = id_info.get("given_name")
        last_name = id_info.get("family_name")
        email = id_info.get("email")
        oauth_provider = "Google"
        oauth_uid = id_info.get("sub")
        oauth_profile_url = id_info.get("picture")

        new_user =  User(first_name=first_name, last_name=last_name, email=email,password="",oauth_provider=oauth_provider,oauth_uid=oauth_uid,oauth_profile_url=oauth_profile_url,is_oauth=True,is_active=True,is_admin=False)
        db.session.add(new_user)
        db.session.commit()
        if new_user.id:
            send_email_welcome(new_user.first_name,new_user.email)
            session[CURR_USER_KEY] = new_user.id
            flash('Your account has been successfully created!','success')
            return redirect(url_for('main.index'))


@bp.route('/authentication', methods=['GET','POST'])
def authentication():
    """authentication view for user login and sign up"""
    tab_one="active"
    tab_selected_one="true"
    tab_show_one="show"

    tab_two=""
    tab_selected_two="false"
    tab_show_two=""

    if g.user:
        return redirect(url_for('main.index'))

    login_form = LoginForm()
    register_form = RegisterForm()


    if request.method == 'POST' and login_form.validate_on_submit():

        tab_one="active"
        tab_selected_one="true"
        tab_show_one="show"

        tab_two=""
        tab_selected_two="false"
        tab_two=""

        email = login_form.login_email.data
        password = login_form.login_password.data
        check_account_type = User.get_users().filter(User.email == email).first()
        if check_account_type:
            if check_account_type.is_oauth:
                flash('This email address is linked to a Google OAuth authentication !','warning')
                return render_template('auth/authentication.html',login_form=login_form,register_form=register_form,
                            tab_one=tab_one,
                            tab_selected_one=tab_selected_one,
                            tab_show_one=tab_show_one,
                            tab_two=tab_two,
                            tab_selected_two=tab_selected_two,
                            tab_show_two=tab_show_two,

                            )

        user = User.login(email = email.casefold(), password = password)
        if user:
            session[CURR_USER_KEY] = user.id
            login_form.login_email.data=""
            login_form.login_password.data=""
            login_form.login_email.errors =""
            flash('Successfully authenticated!','success')
            return redirect(url_for('main.index'))
        else:
            login_form.login_email.errors = ["Email or Password incorrect!"]
            return render_template('auth/authentication.html',login_form=login_form,register_form=register_form,
                        tab_one=tab_one,
                        tab_selected_one=tab_selected_one,
                        tab_show_one=tab_show_one,
                        tab_two=tab_two,
                        tab_selected_two=tab_selected_two,
                        tab_show_two=tab_show_two,

                        )

    if request.method == 'POST' and register_form.validate_on_submit():

        tab_one=""
        tab_selected_one="false"
        tab_show_one=""

        tab_two="active"
        tab_selected_two="true"
        tab_show_two="show"

        register_first_name = register_form.register_first_name.data
        register_last_name = register_form.register_last_name.data
        register_email = register_form.register_email.data
        register_password = register_form.register_password.data
        register_password_confirm = register_form.register_password_confirm.data

        if register_password == register_password_confirm:

            new_user =  User.register(register_first_name, register_last_name, register_email.casefold(), register_password_confirm,False,False)


            if User.get_users().filter(User.email == register_email, User.is_active==True).first():
                register_form.register_email.errors = ["This email address already exists. Please enter another one or reset your password!"]
                return render_template('auth/authentication.html',login_form=login_form,register_form=register_form,
                                tab_one=tab_one,
                                tab_selected_one=tab_selected_one,
                                tab_show_one=tab_show_one,
                                tab_two=tab_two,
                                tab_selected_two=tab_selected_two,
                                tab_show_two=tab_show_two,

                                )
            else:
                user = User.get_users().filter(User.email == register_email, User.is_active == False).first()
                if  user:
                    user.first_name = new_user.first_name
                    user.last_name = new_user.last_name
                    user.password = new_user.password
                    if User.update_users(user):
                        send_email_activation(user.first_name,user.email)
                        return redirect(url_for('auth.activation_notification'))

                else:
                    user_save=User.add_users(new_user)
                    if user_save.id:
                        send_email_activation(user_save.first_name,user_save.email)
                        return redirect(url_for('auth.activation_notification'))
        else:
             register_form.register_password_confirm.errors = ["The two passwords entered are not identical!"]
             return render_template('auth/authentication.html',login_form=login_form,register_form=register_form,
                                tab_one=tab_one,
                                tab_selected_one=tab_selected_one,
                                tab_show_one=tab_show_one,
                                tab_two=tab_two,
                                tab_selected_two=tab_selected_two,
                                tab_show_two=tab_show_two,

                                )


    return render_template('auth/authentication.html',login_form=login_form,register_form=register_form,
                           tab_one=tab_one,
                           tab_selected_one=tab_selected_one,
                           tab_show_one=tab_show_one,
                           tab_two=tab_two,
                           tab_selected_two=tab_selected_two,
                           tab_show_two=tab_show_two,

                           )

@bp.route('/logout',methods=['POST'])
def logout():
    if request.method == 'GET':
        abort(401)

    clear_session()
    return (jsonify("success"), 201)


def clear_session():
     if CURR_USER_KEY in session:
         del session[CURR_USER_KEY]
     session.clear()

@bp.route('/auth/google/callback')
def google_callback():
    pass

@bp.route('/email-reset-password', methods=['GET','POST'])
def email_reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.get_users().filter(User.email == email, User.is_active == True).first()
        if user:
            if user.is_oauth:
                flash('This email address has linked to a Google OAuth authentication and the password cannot be reset in this process!','warning')
                return redirect(url_for('auth.email_reset_password'))
            if send_email_reset_password(user.first_name, user.email):
                return redirect(url_for('auth.send_email_reset_notification'))
        else:
            flash('This email address is not linked to any account!','warning')
            return redirect(url_for('auth.email_reset_password'))

    return render_template('auth/reset_email.html')

@bp.route('reset-user-password/<token>', methods=['GET','POST'])
def reset_user_password(token):
    if request.method == 'GET':
            try:
                email = serializer.loads(token,max_age=120)
                session[EMAIL_RESET] = email
                user = User.get_users().filter(User.email == email, User.is_active == True).first()
                if not user:
                    abort(401)
            except SignatureExpired:
                return redirect(url_for('auth.token_expired_notification'))
            except BadTimeSignature:
                abort(401)
            except Exception:
                return redirect(url_for('auth.token_expired_notification'))
            return render_template('auth/form_reset_change_password.html')

    if request.method == 'POST':
        try:
            new_password= request.form.get('new_password')
            confirm_new_password = request.form.get('confirm_new_password')
            email = session.get(EMAIL_RESET)
            user = User.get_users().filter(User.email == email, User.is_active == True).first()
            if user:
                if new_password != confirm_new_password:
                   flash('The two passwords entered are not identical!','warning')
                   return render_template('auth/form_reset_change_password.html')
                if len(confirm_new_password) < 5:
                    flash('Your passwords should be at least 5 characters long!','warning')
                    return render_template('auth/form_reset_change_password.html')
                user.password = User.hash_function(confirm_new_password)
                if User.update_users(user):
                    if EMAIL_RESET in session:
                        del session[EMAIL_RESET]
                        flash('Your password has been successfully changed!','success')
                        return redirect(url_for('auth.authentication'))
            else:
                return redirect(url_for('auth.token_expired_notification'))
        except SignatureExpired:
                return redirect(url_for('auth.token_expired_notification'))
        except BadTimeSignature:
            abort(401)
        except Exception:
            return redirect(url_for('auth.token_expired_notification'))
    return render_template('auth/form_reset_change_password.html')


@bp.route('/activation-notification')
def activation_notification():
    if g.user:
        return redirect(url_for('main.index'))
    return render_template('auth/activation_notification_page.html')

@bp.route('/send-email-reset-notification')
def send_email_reset_notification():
    if g.user:
        return redirect(url_for('main.index'))
    return render_template('auth/send_email_reset_notification.html')

@bp.route('/link-expired')
def token_expired_notification():
    if g.user:
        return redirect(url_for('main.index'))
    return render_template('auth/token_expired_page.html')



@bp.route('account-activation/<token>', methods=['GET'])
def account_activation(token):
    if request.method == 'GET':
        try:
            email = serializer.loads(token,max_age=600)
            user = User.get_users().filter(User.email == email, User.is_active == False).first()
            if  user:
                user.is_active = True
                if User.update_users(user):
                    session[CURR_USER_KEY] = user.id
                    send_email_welcome(user.first_name,user.email)
                    flash('Your account has been successfully activated!','success')
                    return redirect(url_for('main.index'))
            else:
             return redirect(url_for('auth.token_expired_notification'))
        except SignatureExpired:
            return redirect(url_for('auth.token_expired_notification'))
        except BadTimeSignature:
             abort(401)
        except Exception:
            return redirect(url_for('auth.token_expired_notification'))
    else:
        abort(401)


def send_email_activation(recipient_name,recipient_email):
    try:

        token = serializer.dumps(recipient_email)
        link = url_for('auth.account_activation',token=token,_external=True)
        subject = "Account Activation"

        with open(os.path.join(APP_STATIC, 'mails/account_activation_template.html')) as f:
            html = f.read()

            msg = html.replace('[FIRST_NAME]',recipient_name)
            msg = msg.replace('[APP_LINK]',url_for('main.index',_external=True))
            msg = msg.replace('[LOGO]',url_for('static',filename='images/quick-recipe-logo.png',_external=True))
            msg = msg.replace('[ILLUS]',url_for('static',filename='images/activation.png',_external=True))
            msg = msg.replace('[LINK]',link)
            msg = msg.replace('[GITHUB]',url_for('static',filename='images/github.png',_external=True))
            msg = msg.replace('[LINKEDIN]',url_for('static',filename='images/linkedin.png',_external=True))

            Send_Email(recipient_email,subject,msg,'html')
            flash('A notification has been sent to your e-mail address to activate your account. Please check your mailbox.!','success')
            return True
    except:
        flash('failed!','danger')
        return False

def send_email_reset_password(recipient_name,recipient_email):
    try:

        token = serializer.dumps(recipient_email)
        link = url_for('auth.reset_user_password',token=token,_external=True)
        subject = "Reset Password"

        with open(os.path.join(APP_STATIC, 'mails/password_reset_template.html')) as f:
            html = f.read()

            msg = html.replace('[FIRST_NAME]',recipient_name)
            msg = msg.replace('[APP_LINK]',url_for('main.index',_external=True))
            msg = msg.replace('[LOGO]',url_for('static',filename='images/quick-recipe-logo.png',_external=True))
            msg = msg.replace('[ILLUS]',url_for('static',filename='images/reset-password.png',_external=True))
            msg = msg.replace('[LINK]',link)
            msg = msg.replace('[GITHUB]',url_for('static',filename='images/github.png',_external=True))
            msg = msg.replace('[LINKEDIN]',url_for('static',filename='images/linkedin.png',_external=True))

            Send_Email(recipient_email,subject,msg,'html')
            flash('A notification has been sent to your e-mail address to reset your password. Please check your mailbox.!','success')
            return True
    except:
        flash('failed!','danger')
        return False

def send_email_welcome(recipient_name,recipient_email):
    try:

        subject = "Welcome"

        with open(os.path.join(APP_STATIC, 'mails/welcome_template.html')) as f:
            html = f.read()

            msg = html.replace('[FIRST_NAME]',recipient_name)
            msg = msg.replace('[APP_LINK]',url_for('main.index',_external=True))
            msg = msg.replace('[LINK]',url_for('main.index',_external=True))
            msg = msg.replace('[LOGO]',url_for('static',filename='images/quick-recipe-logo.png',_external=True))
            msg = msg.replace('[ILLUS]',url_for('static',filename='images/welcome.png',_external=True))
            msg = msg.replace('[GITHUB]',url_for('static',filename='images/github.png',_external=True))
            msg = msg.replace('[LINKEDIN]',url_for('static',filename='images/linkedin.png',_external=True))

            Send_Email(recipient_email,subject,msg,'html')
            return True
    except:
        flash('failed!','danger')
        return False
