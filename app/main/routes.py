from app.main import bp
from app.extensions import API_URL_BASE,headers,get_data,render_template,randrange,sample,Json2Object,Object2Json,session,request,g,redirect,url_for,abort,CURR_USER_KEY,db,jsonify,json,convert_json,flash
from app.models.recipe_favorites import RecipeFavorite
from app.models.users import User



def _safe_sample(results, n):
    return sample(results, min(n, len(results)))

@bp.route('/')
def index():
    url = f"{API_URL_BASE}/recipes/list"

    data_recipes_random     = get_data(url, headers=headers, params={"from":"0","size":"20","approved_at":"asc"})
    data_recipes_desert     = get_data(url, headers=headers, params={"from":"0","size":"10","tags":"desserts","approved_at":"asc"})
    data_recipes_vegetarian = get_data(url, headers=headers, params={"from":"0","size":"10","tags":"vegetarian","approved_at":"asc"})
    data_recipes_meat_lover = get_data(url, headers=headers, params={"from":"0","size":"10","tags":"one_top_app_meat","approved_at":"asc"})
    data_recipes_gluten_free= get_data(url, headers=headers, params={"from":"0","size":"10","tags":"gluten_free","approved_at":"asc"})
    data_recipes_african    = get_data(url, headers=headers, params={"from":"0","size":"5","tags":"african","approved_at":"asc"})

    random_recipe       = sample(data_recipes_random.results, 1)[0]
    recipes_desert      = _safe_sample(data_recipes_desert.results, 4)
    recipes_most_popular= _safe_sample(data_recipes_random.results, 5)
    recipes_meat_lover  = _safe_sample(data_recipes_meat_lover.results, 5)
    recipes_gluten_free = _safe_sample(data_recipes_gluten_free.results, 5)
    recipes_vegetarian  = _safe_sample(data_recipes_vegetarian.results, 5)
    recipes_african     = _safe_sample(data_recipes_african.results, 2)

    return render_template('main/index.html', random_recipe=random_recipe, recipes_desert=recipes_desert,
                           recipes_vegetarian=recipes_vegetarian, recipes_most_popular=recipes_most_popular,
                           recipes_meat_lover=recipes_meat_lover, recipes_gluten_free=recipes_gluten_free,
                           recipes_african=recipes_african)

@bp.route('/recipes/favorites')
def recipes_favorites():
    if CURR_USER_KEY not in session:
                abort(401)
    if not g.user:
        return redirect(url_for('main.index'))
    recipe_suggestions=[]

    if g.user.recipe_favorites:
         url = f"{API_URL_BASE}/recipes/list-similarities"
         random_recipe_id_list = [r.recipe_id for r in g.user.recipe_favorites]
         recipe_id = sample(random_recipe_id_list, 1)
         querystring = {"recipe_id":recipe_id}
         recipe_suggestions = get_data(url,headers=headers,params=querystring)
    if recipe_suggestions:
        return render_template('main/favorites.html',recipe_suggestions=recipe_suggestions.results)
    else:
       return render_template('main/favorites.html',recipe_suggestions=recipe_suggestions)

@bp.route('/subscribers')
def get_subscribers():
    if CURR_USER_KEY in session and g.user:
       if not g.user.is_admin:
          abort(401)
       else:
          list_subscribers = User.query.filter(User.is_admin == False)
    else:
         return redirect(url_for('auth.authentication'))

    return render_template('main/subscribers.html',list_subscribers=list_subscribers)

@bp.route('/recipes/pin', methods=["POST"])
def add_pin():
    """Pin and unpin Recipe."""
    if not g.user:
        abort(401)

    if request.method == 'POST':

        data = request.get_data()
        json_object = convert_json(data)
        json_string = json.dumps(json_object)
        final_object = Json2Object(json_string)

        base_data=json_string
        recipe_id=final_object.id
        name=final_object.name
        thumbnail_url=final_object.thumbnail_url
        description=final_object.description
        tag = final_object.tags[0].display_name.replace('_',' ')

        pin = RecipeFavorite.query.filter(RecipeFavorite.user_id==g.user.id,RecipeFavorite.recipe_id==recipe_id).first()

        if pin:
            db.session.delete(pin)
            db.session.commit()

        else:
            pin = RecipeFavorite(user_id=g.user.id,recipe_id=recipe_id,name=name,thumbnail_url=thumbnail_url,description=description,data=base_data,tag=tag)
            db.session.add(pin)
            db.session.commit()

    else:
        abort(401)

    return (jsonify("success"), 201)

@bp.route('/user/profile')
def user_profile():
    if not g.user:
        return redirect(url_for('auth.authentication'))


    return render_template('main/profile.html')

@bp.route('/user/edit-info',methods=['POST'])
def user_edit_info():
    if g.user:
       if request.method == 'POST':
           data = Json2Object(request.get_data())
           first_name = data.first_name
           last_name = data.last_name
           g.user.first_name = first_name
           g.user.last_name = last_name
           db.session.add(g.user)
           db.session.commit()
           return (jsonify("success"), 201)

@bp.route('/user/check-current-pass',methods=['POST'])
def user_check_current_pass():

    if g.user:
       if request.method == 'POST':
           data = Json2Object(request.get_data())
           password = data.curr_password

           if User.hash_function_check(g.user.password,password):
               return (jsonify("success"), 201)
           else:
               return (jsonify("failed"),201)

@bp.route('/user/save-password',methods=['POST'])
def user_save_password():
    if g.user:
       if request.method == 'POST':
           data = Json2Object(request.get_data())
           new_password = data.new_password
           g.user.password = User.hash_function(new_password)
           db.session.add(g.user)
           db.session.commit()
           return (jsonify("success"), 201)

@bp.route('/user/delete-account',methods=['POST'])
def user_delete_account():
    if g.user:
       if request.method == 'POST':
           data = Json2Object(request.get_data())
           email = data.email
           if g.user.email == email:
               db.session.delete(g.user)
               db.session.commit()
               if CURR_USER_KEY in session:
                  del session[CURR_USER_KEY]
                  flash('Account deleted Successfully!','success')
               return (jsonify("success"), 201)
           else:
               return (jsonify("failed"),400)
