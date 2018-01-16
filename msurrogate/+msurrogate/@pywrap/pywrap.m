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
  end
  methods (Access = public)

    function self = pywrap(object)
      self.object = object;
    end


    function [varargout] = subsref(self, ref)
      import msurrogate.*
      switch ref(1).type
          case '.'
            name = ref(1).subs;

            val = py.getattr(self.object, name);

            if not(isempty(ref(2:end)))
              val = py2mat(val);
              [varargout{1:nargout}] = subsref(val, ref(2:end));
             else
               [varargout{1:nargout}] = py2mat(val);
            end
          case '()'
            % function call semantics!
            args_raw = ref(1).subs;

            [args, kwargs] = collectargs(args_raw);
            args = mat2py(args);
            kwargs = mat2py(kwargs);
            val = pyapply(self.object, args, kwargs);
            val = py2mat(val);

            if not(isempty(ref(2:end)))
              [varargout{1:nargout}] = subsref(val, ref(2:end));
            else
              varargout{1} = val;
            end
          case '{}'
            % array access semantics!
            name = ref(1).subs

            %now need to convert to str, single index or index array
            %TODO

            val = py.operator.getitem(self.object, name);
            val = py2mat(val);

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
    [varargout] = mat2py(object)
    [varargout] = py2mat(object)
    val = pyraw(object)
  end
end



