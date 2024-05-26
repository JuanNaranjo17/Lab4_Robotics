
clc; clear; close('all');

L1=10.48;%cm
L2=10.48;%cm
L3=7.576;
L4=5;
syms q1 q2 q3 q4 q5 q6;
%      link     a_i     alpha_i     d_i       Theta_i    offset
datos=[1 ,       0      ,  pi/2 ,      L4      ,    q1   ,     pi/2    ,'R';
        2 ,      L1     ,   0   ,      0      ,    q2   ,     pi/2  ,'R';
        3 ,      L2     ,   0   ,      0      ,    q3   ,      0   ,'R';
        4 ,      L3     ,   0   ,      0      ,    q4   ,      0    ,'R';];
a_i=double(datos(:,2));
alpha_i=double(datos(:,3));
d_i=double(datos(:,4));

offset=double(datos(:,6));
for i=1:1:4
    Esl(i)= Link('revolute', 'd', d_i(i), 'a', a_i(i), 'alpha', alpha_i(i),'offset',offset(i));
end 

Robot1=SerialLink(Esl)
% Robot1.tool=[ 0 0 1 0;
%              -1 0 0 0;
%               0 1 0 0;
%               0 0 0 1]

orientaciones={[0 0 0 0],[25 25 20 -20],[-35 35 -30 30],[85 -20 55 25],[80 -35 55 -45]};
Robots=cell(1,4);
Mat=Robot1.fkine(orientaciones{1});
display('MTH desde la base hasta el EF:')
display(Mat)

figure()
Robot1.name='Posición de Home';
Robot1.teach()
Graficar_Marcos(orientaciones{1},Esl,Robot1)


for i=2:length(orientaciones)
    
    Robots{i}=SerialLink(Esl);
    Robots{i}.name=strcat('Posición',num2str(i));
    figure()
    Robots{i}.plot(orientaciones{i},'workspace',[-30 30 -30 30 -10 50]);
    Graficar_Marcos(orientaciones{i}, Esl,Robots{i})
    
end

function Graficar_Marcos(config, Esl,Robot)

hold on
trplot(eye(4),'rgb','arrow','length',10,'frame','0')
%axis([repmat([-50 50],1,2) 0 60])
M = Esl(1).A(config(1));
trplot(M,'rgb','arrow','frame','1','length',10)
for i=2:Robot.n
    T=Esl(i).A(config(i));
    M = M*T;
    trplot(M,'rgb','arrow','frame',num2str(i),'length',10)
end
hold off

end