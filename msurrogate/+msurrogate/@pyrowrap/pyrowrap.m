%% @deftypefn  {Function File} {} polynomial ()
%% @deftypefnx {Function File} {} polynomial (@var{a})
%% Create a polynomial object representing the polynomial
%%
%% @example
%% @end example
%%
%% @noindent
%% @end deftypefn
classdef pyrowrap < handle
  properties
    async
    object
  end
  methods (Access = public)

    function self = pyrowrap(object, async)
      self.async = async;
      self.object = object;
    end

    function delete(self)
      %should inform pyro that the object is "done"
      try
        %TODO deal with async
        self.object.pyrometa_done()
      catch
        %pass
      end
    end

    function [varargout] = subsref(self, ref)
      import msurrogate.*
      if length(ref) == 3
        disp(length(ref) == 3)
        disp(ref(2).type == '.')
        disp(ref(3).type == '()')
        disp(ref(2).subs == 'async')
      end
      switch ref(1).type
          case '.'
            name = ref(1).subs;

            %this is the method-call form, so don't do the usual subsref recursion and instead do the direct method call
            if all(length(ref) == 2) && all(ref(2).type == '()')

              args_raw = ref(2).subs;
              [args, kwargs] = collectargs(args_raw);

              %insert name to the args here as indexing is different once a python object
              args = mat2py({name, args{:}});
              kwargs = mat2py(kwargs);

              %too dynamic for matlab's interface, so use getattr
              call = py.getattr(self.internal(), 'pyrometa_call');
              val = pyapply(call, args, kwargs);
              [varargout{1:nargout}] = py2mat(val);
              return
            elseif (length(ref) == 3) && all(ref(2).type == '.') && all(ref(3).type == '()') && all(ref(2).subs == 'async')
              args_raw = ref(3).subs;
              [args, kwargs] = collectargs(args_raw);

              %insert name to the args here as indexing is different once a python object
              args = mat2py({name, args{:}});
              kwargs = mat2py(kwargs);

              %too dynamic for matlab's interface, so use getattr
              %TODO MAKE ASYNC
              py.Pyro4.async(self.internal(), true);

              call = py.getattr(self.internal(), 'pyrometa_call');
              val = pyapply(call, args, kwargs);

              py.Pyro4.async(self.internal(), false);
              [varargout{1:nargout}] = pyrowrap(val, true);
              return
            end

            call = py.getattr(self.internal(), 'pyrometa_getattr');
            val = pyapply(call, {name}, struct());

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

            %add None to form the direct call on the object
            args = mat2py({py.None, args{:}});
            kwargs = mat2py(kwargs);

            call = py.getattr(self.internal(), 'pyrometa_call')
            val = pyapply(call, args, kwargs);
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

            call = py.getattr(self.internal(), 'pyrometa_getitem')
            val = pyapply(call, args, struct());
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

          call = py.getattr(self.internal(), 'pyrometa_getattr');
          val = pyapply(call, {name, val}, struct());

          return
        case '{}'
          idx = ref(1).subs;
          idx = mat2py(idx);
          val = mat2py(val);

          call = py.getattr(self.internal(), 'pyrometa_getattr');
          pyapply(call, {idx, val}, struct());
          return
        otherwise
          error('only indexes as a struct/object currently');
      end
    end
  end

  methods (Access = protected)
    function object = internal(self)
      if self.async
        object = self.object.value;
        %TODO check that the return is a proxy and error if not
        self.async = false;
        self.object = object;
      else
        object = self.object;
      end
    end
  end

  methods
    [varargout] = mat2py(object)
    [varargout] = py2mat(object)
    val = pyraw(object)
  end
end



