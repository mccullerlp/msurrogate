%% @deftypefn  {Function File} {} polynomial ()
%% @deftypefnx {Function File} {} polynomial (@var{a})
%% Create a polynomial object representing the polynomial
%%
%% @example
%% @end example
%%
%% @noindent
%% @end deftypefn
classdef pywrap < handle
  properties
    object
    handle
  end
  methods (Access = public)

    function self = pywrap(object, handle)
      self.object = object;
      self.handle = handle;
    end


    function [varargout] = subsref(self, ref)
      import msurrogate.*
      switch ref(1).type
          case '.'
            name = ref(1).subs;

            val = py.getattr(self.object, name);

            if not(isempty(ref(2:end)))
              val = py2mat(val, self.handle);
              [varargout{1:nargout}] = subsref(val, ref(2:end));
             else
               [varargout{1:nargout}] = py2mat(val, self.handle);
            end
          case '()'
            % function call semantics!
            args_raw = ref(1).subs;

            [args, kwargs] = collectargs(args_raw);
            args = mat2py(args);
            kwargs = mat2py(kwargs);
            val = pyapply(self.object, args, kwargs);
            val = py2mat(val, self.handle);

            if not(isempty(ref(2:end)))
              [varargout{1:nargout}] = subsref(val, ref(2:end));
            else
              varargout{1} = val;
            end
          case '{}'
            % array access semantics!
            args_raw = ref(1).subs;

            if length(args_raw) == 1
              args_raw = args_raw{1};
            end

            args = mat2py(args_raw);
            val = py.operator.getitem(self.object, args);
            val = py2mat(val, self.handle);

            if not(isempty(ref(2:end)))
              [varargout{1:nargout}] = subsref(val, ref(2:end));
            else
              [varargout{1:nargout}] = val;
            end
          otherwise
            error('only indexes as a struct/object');
       end
    end

    function self = subsasgn(self, ref, val)
      import msurrogate.*

      if not(isempty(ref(2:end)))
        subself = subsref(self, ref(1:1));
        subsasgn(subself, ref(2:end), val);
        return
      end

      switch ref(1).type
        case '.'
          name = ref(1).subs;
          val = mat2py(val);
          py.setattr(self.object, name, val)
          return
        otherwise
          error('only indexes as a struct/object currently');
      end
    end
  end

  methods
    function map = containers.Map(self)
      map = msurrogate.dict2map(self.object);
    end

    function s = struct(object)
      s = msurrogate.dict2struct(object.object);
    end

    function c = char(object)
      c = char(py.str(object.object));
    end

    function out = dir(object)
      out = msurrogate.py2mat(py.dir(object.object), object.handle);
    end

    function c = disp(object)
      disp(['pywrap[', repr(object), ']']);
    end

    function c = repr(object)
      c = char(py.repr(object.object));
    end

    function val = pyraw(object)
      val = object.object;
    end

    function out = properties(object)
      out = msurrogate.py2mat(py.dir(object.object), object.handle);
    end

    function [varargout] = mat2py(object)
      varargout{1} = object.object;
    end
  end
end



