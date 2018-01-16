function [varargout] = tup2mat(object)
  import msurrogate.*
  ocells = cell(object);
  try
    varargout{1} = cell2mat(ocells);
  catch ME
      switch ME.identifier
      case 'MATLAB:cell2mat:MixedDataTypes'
        varargout{1} = cellfun(@py2mat, ocells, 'UniformOutput', false);
      otherwise
        ME.identifier
        error(ME)
      end
  end
end

