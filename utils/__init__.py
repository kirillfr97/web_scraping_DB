class IFields:
    def __iter__(self):
        for key, value in vars(type(self)).items():
            if not key.startswith('__') and key not in ['values']:
                yield value


class DataFields(IFields):
    Name = 'name'
    HashID = 'hash_id'
    Title = 'title'
    Link = 'link'
    Check = 'checked'
    Created = 'created'
    Description = 'description'


class IssueFields(IFields):
    Level = 'level'
    Created = 'created'
    Message = 'message'
    Link = 'link'
    Content = 'content'
    UserAgent = 'user_agent'
