"""A module for a mixture density network layer

For more info on MDNs, see _Mixture Desity Networks_ by Bishop, 1994.
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.distributions import Categorical
import math

import torch.nn.functional as F
from torch.distributions import Normal, OneHotCategorical


class MixtureDensityNetwork(nn.Module):
    """
    Mixture density network.

    [ Bishop, 1994 ]

    Parameters
    ----------
    dim_in: int; dimensionality of the covariates
    dim_out: int; dimensionality of the response variable
    n_components: int; number of components in the mixture model
    """
    def __init__(self, dim_in, dim_out, n_components):  # n_components 高斯数量
        super().__init__()
        self.pi_network = CategoricalNetwork(dim_in, n_components)
        self.normal_network = MixtureDiagNormalNetwork(dim_in, dim_out,
                                                       n_components)

    def forward(self, x):
        return self.pi_network(x), self.normal_network(x)

    def loss(self, x, y):
        pi, normal = self.forward(x)
        loglik = normal.log_prob(y.unsqueeze(1).expand_as(normal.loc))
        loglik = torch.sum(loglik, dim=2)
        # use pi.logits directly instead of torch.log(pi.probs) to
        # avoid numerical problem
        loss = -torch.logsumexp(pi.logits + loglik, dim=1)
        return loss

    def sample(self, x):
        pi, normal = self.forward(x)
        samples = torch.sum(pi.sample().unsqueeze(2) * normal.sample(), dim=1)
        return samples


class MixtureDiagNormalNetwork(nn.Module):

    def __init__(self, in_dim, out_dim, n_components, hidden_dim=None):
        super().__init__()
        self.n_components = n_components
        if hidden_dim is None:
            hidden_dim = in_dim
        self.network = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, 2 * out_dim * n_components),
        )

    def forward(self, x):
        params = self.network(x)
        mean, sd = torch.split(params, params.shape[1] // 2, dim=1) #相当于把params分成左右两个大小相等的矩阵
        mean = torch.stack(mean.split(mean.shape[1] // self.n_components, 1))
        sd = torch.stack(sd.split(sd.shape[1] // self.n_components, 1))
        # replaced torch.exp(sd) with ELU plus to improve numerical stability
        # added epsilon to avoid zero scale
        # due to non associativity of floating point add, 1 and 1e-7 need to be added seperately
        return Normal(mean.transpose(0, 1), (F.elu(sd)+1+1e-7).transpose(0, 1))#transpose(0,1) 为矩阵转置

class CategoricalNetwork(nn.Module):

    def __init__(self, in_dim, out_dim, hidden_dim=None):
        super().__init__()
        if hidden_dim is None:
            hidden_dim = in_dim
        self.network = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, out_dim)
        )

    def forward(self, x):
        params = self.network(x)
        return OneHotCategorical(logits=params)


ONEOVERSQRT2PI = 1.0 / math.sqrt(2 * math.pi)


class MDN(nn.Module):
    """A mixture density network layer

    The input maps to the parameters of a MoG probability distribution, where
    each Gaussian has O dimensions and diagonal covariance.

    Arguments:
        in_features (int): the number of dimensions in the input
        out_features (int): the number of dimensions in the output
        num_gaussians (int): the number of Gaussians per output dimensions

    Input:
        minibatch (BxD): B is the batch size and D is the number of input
            dimensions.

    Output:
        (pi, sigma, mu) (BxG, BxGxO, BxGxO): B is the batch size, G is the
            number of Gaussians, and O is the number of dimensions for each
            Gaussian. Pi is a multinomial distribution of the Gaussians. Sigma
            is the standard deviation of each Gaussian. Mu is the mean of each
            Gaussian.
    """
    def __init__(self, in_features, out_features, num_gaussians):       #二维高斯分布
        super(MDN, self).__init__()                                     #高斯分布的系数
        self.in_features = in_features      #输入维数
        self.out_features = out_features    #输出维数
        self.num_gaussians = num_gaussians  #高斯分布的个数
        self.pi_x = nn.Sequential(            #创建pi_x神经元
            nn.Linear(in_features, num_gaussians),
            nn.Softmax(dim=1)
        )
        self.pi_y = nn.Sequential(            #创建pi_y神经元
            nn.Linear(in_features, num_gaussians),
            nn.Softmax(dim=1)
        )
        self.sigma_x = nn.Linear(in_features, out_features * num_gaussians)     #创建sigma_x神经元
        self.sigma_y = nn.Linear(in_features, out_features * num_gaussians)     #创建sigma_y神经元
        self.mu_x = nn.Linear(in_features, out_features * num_gaussians)        #创建mu_x神经元
        self.mu_y = nn.Linear(in_features, out_features * num_gaussians)        #创建mu_y神经元

    def forward(self, minibatch):
        pi_x = self.pi_x(minibatch)
        pi_y = self.pi_y(minibatch) #
        sigma_x = torch.exp(self.sigma_x(minibatch))
        sigma_x = sigma_x.view(-1, self.num_gaussians, self.out_features)
        sigma_y = torch.exp(self.sigma_y(minibatch))
        sigma_y = sigma_y.view(-1, self.num_gaussians, self.out_features)
        mu_x = self.mu_x(minibatch)
        mu_x = mu_x.view(-1, self.num_gaussians, self.out_features)
        mu_y = self.mu_y(minibatch)
        mu_y = mu_y.view(-1, self.num_gaussians, self.out_features)
        return pi_x, pi_y, sigma_x, sigma_y, mu_x, mu_y






    # def __init__(self, in_features, out_features, num_gaussians):
    #     super(MDN, self).__init__()
    #     self.in_features = in_features      #输入维数
    #     self.out_features = out_features    #输出维数
    #     self.num_gaussians = num_gaussians  #高斯分布的个数
    #     self.pi = nn.Sequential(            #创建神经层
    #         nn.Linear(in_features, num_gaussians),
    #         nn.Softmax(dim=1)
    #     )
    #     self.sigma = nn.Linear(in_features, out_features * num_gaussians)     #方差的个数，输出维数*高斯分布的个数
    #     self.mu = nn.Linear(in_features, out_features * num_gaussians)        #均值的个数，输出维数*高斯分布的个数
    #
    # def forward(self, minibatch):
    #     pi = self.pi(minibatch)             #
    #     sigma = torch.exp(self.sigma(minibatch))
    #     sigma = sigma.view(-1, self.num_gaussians, self.out_features)
    #     mu = self.mu(minibatch)
    #     mu = mu.view(-1, self.num_gaussians, self.out_features)
    #     return pi, sigma, mu


def gaussian_probability(sigma, mu, target):
    """Returns the probability of `target` given MoG parameters `sigma` and `mu`.

    Arguments:
        sigma (BxGxO): The standard deviation of the Gaussians. B is the batch
            size, G is the number of Gaussians, and O is the number of
            dimensions per Gaussian.
        mu (BxGxO): The means of the Gaussians. B is the batch size, G is the
            number of Gaussians, and O is the number of dimensions per Gaussian.
        target (BxI): A batch of target. B is the batch size and I is the number of
            input dimensions.

    Returns:
        probabilities (BxG): The probability of each point in the probability
            of the distribution in the corresponding sigma/mu index.
    """
    sigma = F.elu(sigma)+1+1e-7
    target = target.unsqueeze(1).expand_as(sigma)
    ret = ONEOVERSQRT2PI * torch.exp(-0.5 * ((target - mu) / sigma)**2) / sigma
    return torch.prod(ret, 2)


def mdn_loss(pi_x, pi_y, sigma_x, sigma_y, mu_x, mu_y, target_x, target_y):
    """Calculates the error, given the MoG parameters and the target

    The loss is the negative log likelihood of the data given the MoG
    parameters.
    """
    prob_x = pi_x * gaussian_probability(sigma_x, mu_x, target_x)  * gaussian_probability(sigma_y, mu_y, target_y)             #分别计算x和y和概率
    #prob_y = pi_y * gaussian_probability(sigma_y, mu_y, target_y)

    #nll = -torch.log(torch.sum(prob_x, dim=1))-torch.log( torch.sum(prob_y, dim=1))        #返回损失和
    nll = -torch.log(torch.sum(prob_x, dim=1))
    return torch.mean(nll)


def sample(pi, sigma, mu):
    """Draw samples from a MoG.
    """
    # Choose which gaussian we'll sample from
    pis = Categorical(pi).sample().view(pi.size(0), 1, 1)
    # Choose a random sample, one randn for batch X output dims
    # Do a (output dims)X(batch size) tensor here, so the broadcast works in
    # the next step, but we have to transpose back.
    gaussian_noise = torch.randn(
        (sigma.size(2), sigma.size(0)), requires_grad=False)
    variance_samples = sigma.gather(1, pis).detach().squeeze()
    mean_samples = mu.detach().gather(1, pis).squeeze()
    return (gaussian_noise * variance_samples + mean_samples).transpose(0, 1)
