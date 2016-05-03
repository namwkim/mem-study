

load('gdesign30x50.mat');
im_maps = dir('./gd_imp');
mkdir('gd_imp_mturk');
mkdir('gd_person_mturk');
mkdir('gd_text_mturk');

for i=1:length(bubble)
    bubble(i).filename;
    [pathstr,name,ext] = fileparts(bubble(i).filename);
    
    copyfile(strcat('./gd_imp/',name, '.png'), strcat('./gd_imp_mturk/',name, '.png'));
    source = strcat('./gd_person_info/',name, '-face.mat');
    if exist(source, 'file') == 2
        copyfile(source, strcat('./gd_person_mturk/',name, '-face.mat'));
    end
    source = strcat('./gd_person_info/',name, '-people.mat');
    if exist(source, 'file') == 2        
        copyfile(source, strcat('./gd_person_mturk/',name, '-people.mat'));
    end
    source = strcat('./gd_text_info/',name, '.mat');
    if exist(source, 'file') == 2        
        copyfile(source, strcat('./gd_text_mturk/',name, '.mat'));
    end     
end