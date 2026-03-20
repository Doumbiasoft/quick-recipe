from app.extensions import render_template,redirect,flash,url_for,abort,request,API_URL_BASE,headers,get_data,Json2Object,Object2Json,session,convert_json,jsonify,json,RECIPE_ITEM
from app.search import bp
from app.forms.search.recipes import SearchForm


url = f"{API_URL_BASE}/recipes/list"
url_tags = f"{API_URL_BASE}/tags/list"
data_tags = get_data(url_tags,headers=headers)
tags = data_tags.results


@bp.route('/recipes', methods=['GET','POST'])
def recipes():
    """Search view"""

    querystring = {"from":"0","size":"20","approved_at":"asc"}

    form = SearchForm()
    form.tags.choices = get_tag_tuple()
    if request.method == 'POST':
        if form.validate_on_submit():

            recipe = form.recipe.data
            tag = form.tags.data

            if tag is not None:
                querystring["tags"] = tag.lower()
                querystring["size"] = "100"
            if recipe is not None:
                querystring["q"] = recipe.lower()
                querystring["size"] = "100"


            data_recipes_found = get_data(url,headers=headers,params=querystring)
            if tag is not None or recipe is not None:
                recipes_found = data_recipes_found.results
            elif tag is None and recipe is None:
                recipes_found = data_recipes_found.results
            return render_template('search/recipes.html',recipes_found=recipes_found,form=form)

    data_recipes_found = get_data(url,headers=headers,params=querystring)
    recipes_found = data_recipes_found.results

    return render_template('search/recipes.html',recipes_found=recipes_found,form=form)

@bp.route('/recipes-item', methods=['POST'])
def recipes_item():
    """Detail recipe view"""
    if request.method == 'POST':

        data = request.get_data()
        json_object = convert_json(data)
        json_string = json.dumps(json_object)
        session[RECIPE_ITEM] = json_string
    else:
        abort(401)

    return (jsonify("success"), 201)



@bp.route('/recipes/details/<int:recipe_id>', methods=['GET'])
def recipes_details(recipe_id):
    """Detail recipe view"""
    if RECIPE_ITEM in session:
        json_object = session.get(RECIPE_ITEM)
        json_string = json.dumps(json_object)
        json_object = Json2Object(json_string)
        recipe = Json2Object(json_object)
    else:
        abort(401)

    return render_template('search/details.html',recipe=recipe)



def get_type():
    seen = set()
    unique_list = []
    for obj in tags:
        if obj.type not in seen:
            unique_list.append({"id":f"{obj.type}","name":f"{obj.type.replace('_',' ')}"})
            seen.add(obj.type)
    return unique_list

def get_tag_by_type(type:str):
    seen = set()
    unique_list = []
    for obj in tags:
        if obj.type == type:
            if obj.name not in seen:
               unique_list.append({"id":f"{obj.name}","name":f"{obj.display_name.lower()}"})
               seen.add(obj.name)
    return unique_list

def get_tag():
    seen = set()
    unique_list = []
    for obj in tags:
        if obj.name not in seen:
            unique_list.append({"id":f"{obj.name}","name":f"{obj.display_name.lower()}"})
            seen.add(obj.name)
    return unique_list

def get_tag_tuple():
    seen = set()
    unique_list = []
    unique_list.append(("","-- Tags --"))
    for obj in tags:
        if obj.name not in seen:
            unique_list.append((f"{obj.name}",f"{obj.display_name.lower()}"))
            seen.add(obj.name)
    return sort_tuple(unique_list)

def sort_tuple(tup):

    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    return(sorted(tup, key = lambda x: x[1]))
