1. 
```
UPDATE full_names 
SET status = short_names.status 
FROM short_names 
WHERE short_names.name = split_part(full_names.name, '.', 1);
```

2. 
```
UPDATE full_names 
SET status = short_names.status 
FROM short_names 
WHERE full_names.name ~ ('^' || short_names.name || '\.[a-zA-Z0-9]+$'); 
```

3. 
```
UPDATE full_names 
SET status = short_names.status 
FROM short_names 
WHERE short_names.name = substring(full_names.name from 1 for  position('.' in full_names.name)-1);
```
