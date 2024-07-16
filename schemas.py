from marshmallow import Schema, fields


    

class PlainUserschema(Schema):
    status  = fields.Str(dump_only=True)
    dd = fields.Str(dump_only=True)
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role_id = fields.Int(required=True)
    phone_number = fields.Int(required =True)
    password = fields.Str(required=True, load_only=True)
    # total_pages = fields.Int(dump_only = True)
    # prev_page = fields.Int(dump_only = True)
    # next_page = fields.Int(dump_only = True)
    #meta = fields.Dict(fields.Str(),values=fields.Int())

class Forall(PlainUserschema):
    status  = fields.Str(dump_only=True)
    dd = fields.Str(dump_only=True)
    data = fields.List(fields.Nested(PlainUserschema()), dump_only = True)

class PlainReviewSchema(Schema):

    id = fields.Int(dump_only=True)
    brandname = fields.Str(required=True)
    product = fields.Str(required=True)
    review = fields.Str(required=True)
    files = fields.Str(required=True)
    rating = fields.Int(required=True)

class ReviewSchema(PlainReviewSchema):
     user_id = fields.Int(load_only=True)
     status = fields.Str(required=True)
     message = fields.Str(required=True) 
     user = fields.Nested(PlainUserschema(), dump_only = True)
     likee = fields.List(fields.Nested(PlainUserschema()), dump_only = True)

class TestReview(ReviewSchema):
    pass
    #status = fields.Str(dump_only = True)
    #message = fields.Str(dump_only = True)
    #body = fields.List(fields.Nested(ReviewSchema()), dump_only = True)
   

class Userschema(PlainUserschema):
    reviews = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)
    #followers = fields.List(fields.Nested(PlainUserschema()), dump_only=True)
    like = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)


class UserUpdateSchema(Schema):
    name =fields.Str()
    email = fields.Email()
    role_id =fields.Int()
    phone_number = fields.Str()
    password = fields.Str(required=True, load_only=True)

class RoleSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)
    status = fields.Int(dump_only = True)
    #permissions = fields.List(fields.Dict(keys=fields.Str(), values=fields.Dict(keys=fields.Str(),values=fields.Int())),required = True)

class RoleUpdateSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str()
    status = fields.Int(dump_only = True)
    # = fields.List(fields.Dict(keys=fields.Str(), values=fields.Dict(keys=fields.Str(),values=fields.Int())))

class PermissionSchema(Schema):
    id = fields.Int(dump_only = True)
    role_id = fields.Int(required=True)
    permissions = fields.List(fields.Dict(keys=fields.Str(), values=fields.Dict(keys=fields.Str(),values=fields.Int())),required = True)


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    id = fields.Int(dump_only = True)
    access_token = fields.Str(dump_only=True)

class FilterSchema(Schema):
    filter = fields.Str(required=True)
    brand = fields.Str()

class FileformSchema(Schema):
    #file = fields.Raw(type='file')
    name = fields.Str()
    title = fields.Str()


class SupporterSchema(Schema):
     user_id = fields.Int(required=True)
     suppoter_id = fields.Int(required=True)


class LikeAndReviewSchema(Schema):
     message = fields.Str()
     user = fields.Nested(Userschema)
     review = fields.Nested(ReviewSchema)

class ReviewLikeSchema(Schema):
     user_id = fields.Int(required=True)
     review_id = fields.Int(required=True)





