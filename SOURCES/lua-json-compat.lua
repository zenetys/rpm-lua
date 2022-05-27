-- Incomplete compatibility layer for lua-json
-- https://github.com/harningt/luajson

local _G = _G
local cjson = require 'cjson.safe'
_G.json = cjson
return cjson
