function data = jsondecode(json)
    if exist('jsondecode')
        data = jsondecode(json);
    else
        data = iirrational.json.parse_json(json);
        data = data{1};
    end
end
